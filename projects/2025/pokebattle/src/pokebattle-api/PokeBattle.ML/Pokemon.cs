using Microsoft.ML.Data;

namespace PokeBattle.ML;

public class Pokemon
{
    [LoadColumn(29)]
    public string Name { get; set; }
    [LoadColumn(27)]
    public float Hp { get; set; }
    [LoadColumn(18)]
    public float Attack { get; set; }
    [LoadColumn(32)]
    public float SpecialAttack { get; set; }
    [LoadColumn(24)]
    public float Defense { get; set; }
    [LoadColumn(33)]
    public float SpecialDefence { get; set; }
    [LoadColumn(34)]
    public float Speed { get; set; }
    [LoadColumn(21)]
    public float BaseTotal { get; set; }
    [LoadColumn(22)]
    public float CaptureRate { get; set; }
    [LoadColumn(35)]
    public string Type1 { get; set; }
    [LoadColumn(36)]
    public string? Type2 { get; set; }
    [LoadColumn(38)]
    public float Generation { get; set; }
    [LoadColumn(39)]
    public bool IsLegendary { get; set; }
}