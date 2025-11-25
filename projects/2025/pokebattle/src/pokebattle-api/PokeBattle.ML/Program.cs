using PokeBattle.ML;

const string source = "/home/mborto/Repos/PokeBattle/data/pokemon.csv";

// Test with a sample Pokemon
var rillaboom = new Pokemon
{
    Hp = 100,
    Attack = 125,
    Defense = 90,
    SpecialAttack = 60,
    SpecialDefence = 70,
    Speed = 85,
    Type1 = "grass",
    IsLegendary = false
};

var zacian = new Pokemon
{
    Hp = 92,
    Attack = 120,
    Defense = 115,
    SpecialAttack = 80,
    SpecialDefence = 115,
    Speed = 138,
    Type1 = "fairy",
    IsLegendary = true
};

var eter = new Pokemon
{
    Hp = 140,
    Attack = 85,
    Defense = 95,
    SpecialAttack = 145,
    SpecialDefence = 95,
    Speed = 130,
    Type1 = "poison",
    Type2 = "dragon",
    IsLegendary = true
};
var grookey = new Pokemon
{
    Hp = 50,
    Attack = 65,
    Defense = 50,
    SpecialAttack = 40,
    SpecialDefence = 40,
    Speed = 65,
    Type1 = "grass",
    IsLegendary = false
};
var manafy = new Pokemon
{
    Hp = 100,
    Attack = 100,
    Defense = 100,
    SpecialAttack = 100,
    SpecialDefence = 100,
    Speed = 100,
    Type1 = "water",
    IsLegendary = true
};

var dragapult = new Pokemon
{
    Hp = 88,
    Attack = 120,
    Defense = 75,
    SpecialAttack = 100,
    SpecialDefence = 75,
    Speed = 142,
    Type1 = "dragon",
    Type2 = "ghost",
    IsLegendary = false
};
/* PREDICT TYPE * /
/*
const string modelPath = "/home/mborto/Repos/PokeBattle/data/predict-type.zip";
var predictTypeModel = new PredictTypeModel(modelPath, source);
var predictedType = predictTypeModel.PredictTypeModel(testPokemon)
*/

/* PREDICT TOTAL STATS */
/*
const string totalStatsModelPath = "/home/mborto/Repos/PokeBattle/data/predict-total-stats.zip";
var predictTotalStatsModel = new PredictTotalStatsModel(totalStatsModelPath, source);
var predictedTotal = predictTotalStatsModel.PredictTotalStat(testPokemon);
*/

/* PREDICT LEGENDARY */
/*
const string legendaryModelPath = "/home/mborto/Repos/PokeBattle/data/predict-legendary.zip";
var predictTotalStatsModel = new PredictLegendaryModel(legendaryModelPath, source);
var isLegendary = predictTotalStatsModel.PredictLegendary(grookey);
*/

const string legendaryModelPath = "/home/mborto/Repos/PokeBattle/data/predict-catchrate.zip";
var predictTotalStatsModel = new PredictCatchRateModel(legendaryModelPath, source);

// Test multiple Pokémon to see the pattern
Console.WriteLine("\n--- Testing Multiple Pokémon ---");
Console.WriteLine($"Grookey (not legendary): {predictTotalStatsModel.PredictCatchRate(grookey)}");
Console.WriteLine($"Rillaboom (not legendary): {predictTotalStatsModel.PredictCatchRate(rillaboom)}");
Console.WriteLine($"Zacian (legendary): {predictTotalStatsModel.PredictCatchRate(zacian)}");
Console.WriteLine($"Eternatus (legendary): {predictTotalStatsModel.PredictCatchRate(eter)}");
Console.WriteLine($"Manafy (legendary): {predictTotalStatsModel.PredictCatchRate(manafy)}");
Console.WriteLine($"Dragapult (not legendary): {predictTotalStatsModel.PredictCatchRate(dragapult)}");