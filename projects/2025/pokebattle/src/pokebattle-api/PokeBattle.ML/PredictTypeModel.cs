using Microsoft.ML;
using Microsoft.ML.Data;

namespace PokeBattle.ML;

public class TypePrediction
{
    [ColumnName("PredictedLabel")]
    public string PredictedType;
}

public class PredictTypeModel(string modelPath, string sourcePath)
{
    public string PredictType(Pokemon pokemon)
    {
        ITransformer trainedModel;

        var mlContext = new MLContext(seed: 0);

        if (File.Exists(modelPath))
        {
            trainedModel = mlContext.Model.Load(modelPath, out var schema);
        }
        else
        {
            var trainingDataView = mlContext.Data.LoadFromTextFile<Pokemon>(
                sourcePath, hasHeader: true, separatorChar: ',');

            var pipeline = ProcessData(mlContext);
            var trainingPipeline = BuildAndTrainModel(mlContext, pipeline);

            trainedModel = trainingPipeline.Fit(trainingDataView);
            mlContext.Model.Save(trainedModel, trainingDataView.Schema, modelPath);
        }

        var predEngine = mlContext.Model.CreatePredictionEngine<Pokemon, TypePrediction>(trainedModel);

        var prediction = predEngine.Predict(pokemon);
        return prediction.PredictedType;
    }

    private static IEstimator<ITransformer> ProcessData(MLContext mlContext)
    {
        var pipeline =
            // Convert Type1 to number and map to Label (output)
            mlContext.Transforms.Conversion.MapValueToKey(inputColumnName: "Type1", outputColumnName: "Label")
                // Concat stats into Feature (input)
                .Append(mlContext.Transforms.Concatenate("Features",
                    nameof(Pokemon.Hp),
                    nameof(Pokemon.Attack),
                    nameof(Pokemon.SpecialAttack),
                    nameof(Pokemon.Defense),
                    nameof(Pokemon.SpecialDefence),
                    nameof(Pokemon.Speed)))
                .AppendCacheCheckpoint(mlContext);
        return pipeline;
    }

    private static IEstimator<ITransformer> BuildAndTrainModel(MLContext mlContext, IEstimator<ITransformer> pipeline)
    {
        var trainingPipeline = pipeline
            .Append(mlContext.MulticlassClassification.Trainers.SdcaMaximumEntropy("Label", "Features"))
            .Append(mlContext.Transforms.Conversion.MapKeyToValue("PredictedLabel"));
        return trainingPipeline;
    }
}