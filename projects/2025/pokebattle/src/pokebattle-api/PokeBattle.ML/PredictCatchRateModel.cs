using Microsoft.ML;
using Microsoft.ML.Data;

namespace PokeBattle.ML;

public class CatchRatePrediction
{
    [ColumnName("Score")]
    public float PredictedCatchRate;
}

public class PredictCatchRateModel(string modelPath, string sourcePath)
{
    public float PredictCatchRate(Pokemon pokemon)
    {
        ITransformer trainedModel;

        var mlContext = new MLContext(seed: 0);

        if (File.Exists(modelPath))
        {
            trainedModel = mlContext.Model.Load(modelPath, out var schema);
        }
        else
        {
            var dataView = mlContext.Data.LoadFromTextFile<Pokemon>(
                sourcePath, hasHeader: true, separatorChar: ',');

            // Debug: Check the data
            var preview = dataView.Preview(maxRows: 10);
            Console.WriteLine("\n=== Sample Training Data ===");
            foreach (var row in preview.RowView)
            {
                var captureRate = row.Values.FirstOrDefault(v => v.Key == "CaptureRate").Value;
                var isLegendary = row.Values.FirstOrDefault(v => v.Key == "IsLegendary").Value;
                var hp = row.Values.FirstOrDefault(v => v.Key == "Hp").Value;
                Console.WriteLine($"CaptureRate: {captureRate}, IsLegendary: {isLegendary}, HP: {hp}");
            }
            // Split data 80/20 for training and testing
            var trainTestSplit = mlContext.Data.TrainTestSplit(dataView, testFraction: 0.2, seed: 0);

            var pipeline = ProcessData(mlContext);
            var trainingPipeline = BuildAndTrainModel(mlContext, pipeline);

            Console.WriteLine("\nTraining model...");
            trainedModel = trainingPipeline.Fit(trainTestSplit.TrainSet);
            
            // Evaluate the model on test data
            var predictions = trainedModel.Transform(trainTestSplit.TestSet);
            var metrics = mlContext.Regression.Evaluate(predictions, labelColumnName: "Label", scoreColumnName: "Score");
            
            Console.WriteLine($"\nModel trained and evaluated:");
            Console.WriteLine($"  R^2: {metrics.RSquared:0.###}");
            Console.WriteLine($"  MAE: {metrics.MeanAbsoluteError:0.###}");
            Console.WriteLine($"  RMSE: {metrics.RootMeanSquaredError:0.###}");
            
            mlContext.Model.Save(trainedModel, dataView.Schema, modelPath);
            Console.WriteLine($"\nModel saved to: {modelPath}");
        }

        var predEngine = mlContext.Model.CreatePredictionEngine<Pokemon, CatchRatePrediction>(trainedModel);

        var prediction = predEngine.Predict(pokemon);
        return prediction.PredictedCatchRate;
    }

    private static IEstimator<ITransformer> ProcessData(MLContext mlContext)
    {
        var pipeline =
            mlContext.Transforms.CopyColumns(inputColumnName: nameof(Pokemon.CaptureRate), outputColumnName: "Label")
                .Append(mlContext.Transforms.Conversion.ConvertType(
                    outputColumnName: "IsLegendaryFloat",
                    inputColumnName: nameof(Pokemon.IsLegendary),
                    outputKind: DataKind.Single))
                .Append(mlContext.Transforms.Concatenate("Features",
                    nameof(Pokemon.Hp),
                    nameof(Pokemon.Attack),
                    nameof(Pokemon.SpecialAttack),
                    nameof(Pokemon.Defense),
                    nameof(Pokemon.SpecialDefence),
                    nameof(Pokemon.Speed),
                    "IsLegendaryFloat"));
        return pipeline;
    }

    private static IEstimator<ITransformer> BuildAndTrainModel(MLContext mlContext, IEstimator<ITransformer> pipeline)
    {
        var trainingPipeline = pipeline
            .Append(mlContext.Regression.Trainers.Sdca(
                labelColumnName: "Label",
                featureColumnName: "Features"));
        return trainingPipeline;
    }
}
