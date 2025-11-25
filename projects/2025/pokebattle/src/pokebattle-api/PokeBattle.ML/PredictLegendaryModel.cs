using Microsoft.ML;
using Microsoft.ML.Data;

namespace PokeBattle.ML;

public class LegendaryPrediction
{
    [ColumnName("PredictedLabel")] public bool IsLegendary { get; set; }

    public float Probability { get; set; }

    public float Score { get; set; }
}

public class PredictLegendaryModel(string modelPath, string sourcePath)
{
    public bool PredictLegendary(Pokemon pokemon)
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
            var metrics = mlContext.BinaryClassification.Evaluate(predictions, labelColumnName: "Label");

            Console.WriteLine($"\nModel Evaluation Metrics:");
            Console.WriteLine($"Accuracy: {metrics.Accuracy:P2}");
            Console.WriteLine($"AUC: {metrics.AreaUnderRocCurve:P2}");
            Console.WriteLine($"F1 Score: {metrics.F1Score:P2}");

            mlContext.Model.Save(trainedModel, dataView.Schema, modelPath);
            Console.WriteLine($"\nModel saved to: {modelPath}");
        }

        var predEngine = mlContext.Model.CreatePredictionEngine<Pokemon, LegendaryPrediction>(trainedModel);

        var prediction = predEngine.Predict(pokemon);
        return prediction.IsLegendary;
    }

    private static IEstimator<ITransformer> ProcessData(MLContext mlContext)
    {
        var pipeline =
            mlContext.Transforms.CopyColumns(inputColumnName: nameof(Pokemon.IsLegendary), outputColumnName: "Label")
                .Append(mlContext.Transforms.Text.FeaturizeText(inputColumnName: "Type1", outputColumnName: "Type1Featurized"))
                .Append(mlContext.Transforms.Text.FeaturizeText(inputColumnName: "Type2", outputColumnName: "Type2Featurized"))
                .Append(mlContext.Transforms.Concatenate("Features",
                    nameof(Pokemon.Hp),
                    nameof(Pokemon.Attack),
                    nameof(Pokemon.SpecialAttack),
                    nameof(Pokemon.Defense),
                    nameof(Pokemon.SpecialDefence),
                    nameof(Pokemon.Speed),
                    "Type1Featurized",
                    "Type2Featurized"));
        return pipeline;
    }

    private static IEstimator<ITransformer> BuildAndTrainModel(MLContext mlContext, IEstimator<ITransformer> pipeline)
    {
        var trainingPipeline = pipeline
            .Append(mlContext.BinaryClassification.Trainers.LbfgsLogisticRegression(
                labelColumnName: "Label",
                featureColumnName: "Features",
                l1Regularization: 0.1f,
                l2Regularization: 0.1f));
        return trainingPipeline;
    }
}