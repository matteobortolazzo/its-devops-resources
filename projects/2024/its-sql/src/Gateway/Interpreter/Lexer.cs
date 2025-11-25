using System.Text.Json.Serialization;

namespace Gateway.Interpreter;

[JsonConverter(typeof(JsonStringEnumConverter))]
public enum TokenType
{
    Keyword,
    Identifier,
    String,
    Number,
    Operator,
    Null
}

public record Token(TokenType Type, string Value);

public class Lexer
{
    private static readonly char[] Operators = ['=', '*', ',', '>', '<'];
    private static readonly string[] Keyword = ["SELECT", "FROM", "WHERE", "AND", "OR"];

    public Token[] Tokenize(string input)
    {
        var tokens = new List<Token>();
        var current = 0;
        while (current < input.Length)
        {
            var c = input[current];
            if (char.IsWhiteSpace(c))
            {
                current++;
                continue;
            }

            if (char.IsLetter(c))
            {
                var start = current;
                while (current < input.Length && char.IsLetterOrDigit(input[current]))
                {
                    current++;
                }

                var value = input[start..current];

                var type = TokenType.Identifier;
                if (Keyword.Contains(value))
                {
                    type = TokenType.Keyword;
                }
                else if (value == "NULL")
                {
                    type = TokenType.Null;
                }

                tokens.Add(new Token(type, value));
                continue;
            }

            if (char.IsDigit(c))
            {
                var start = current;
                while (current < input.Length && char.IsDigit(input[current]))
                {
                    current++;
                }

                var value = input[start..current];
                tokens.Add(new Token(TokenType.Number, value));
                continue;
            }

            if (Operators.Contains(c))
            {
                tokens.Add(new Token(TokenType.Operator, c.ToString()));
                current++;
                continue;
            }

            if (c == '\'')
            {
                var start = current + 1;
                current++;
                while (current < input.Length && input[current] != '\'')
                {
                    current++;
                }

                var value = input[start..current];
                tokens.Add(new Token(TokenType.String, value));
                current++;
            }
        }

        return tokens.ToArray();
    }
}