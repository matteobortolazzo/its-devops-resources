namespace PokeBattle.ApiService;

public enum PokemonType
{
    Grass,
    Fire,
    Water,
    Fighting,
    Poison,
    Electric,
    Ground,
    Flying,
    Psychic,
    Bug,
    Rock,
    Ice,
    Dark,
    Steel,
    Dragon,
    Normal,
    Ghost,
    Fairy
}

public class BattleService
{
    public bool WillWinAgainFire(PokemonType opponentType)
    {
        return opponentType switch
        {
            PokemonType.Water => true,
            PokemonType.Ground => true,
            PokemonType.Rock => true,
            _ => false
        };
    }
}