using PokeBattle.ApiService;

namespace Pokebattle.UnitTests;

public class BattleServiceTests
{
    private readonly BattleService _service = new();
    
    [Theory]
    [InlineData(PokemonType.Water, true)]
    [InlineData(PokemonType.Dark, false)]
    [InlineData(PokemonType.Fire, false)]
    [InlineData(PokemonType.Electric, false)]
    [InlineData(PokemonType.Grass, false)]
    [InlineData(PokemonType.Fighting, false)]
    [InlineData(PokemonType.Rock, true)]
    public void TestWin(PokemonType opponentType, bool expectedResult)
    {
        var result = _service.WillWinAgainFire(opponentType);
        Assert.Equal(expectedResult, result);
    }
}