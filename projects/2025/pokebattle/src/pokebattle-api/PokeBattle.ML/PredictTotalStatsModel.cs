using Microsoft.ML;
using Microsoft.ML.Data;

namespace PokeBattle.ML;

public class TotalStatPrediction
{
    [ColumnName("Score")]
    public float PredictedTotalStat;
}

public class PredictTotalStatsModel(string modelPath, string sourcePath)
{
    public int PredictTotalStat(Pokemon pokemon)
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

        var predEngine = mlContext.Model.CreatePredictionEngine<Pokemon, TotalStatPrediction>(trainedModel);

        var prediction = predEngine.Predict(pokemon);
        return (int)Math.Round(prediction.PredictedTotalStat);
    }

    private static IEstimator<ITransformer> ProcessData(MLContext mlContext)
    {
        var pipeline =
            mlContext.Transforms.CopyColumns(inputColumnName: nameof(Pokemon.BaseTotal), outputColumnName: "Label")
                .Append(mlContext.Transforms.Concatenate("Features",
                    nameof(Pokemon.Hp),
                    nameof(Pokemon.Attack),
                    nameof(Pokemon.SpecialAttack),
                    nameof(Pokemon.Defense),
                    nameof(Pokemon.SpecialDefence),
                    nameof(Pokemon.Speed)))
                .Append(mlContext.Transforms.NormalizeMinMax("Features"));
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
