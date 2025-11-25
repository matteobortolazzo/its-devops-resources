export enum TokenKind {
    LeftBrace = 'LeftBrace',
    RightBrace = 'RightBrace',
    LeftBracket = 'LeftBracket',
    RightBracket = 'RightBracket',
    Colon = 'Colon',
    Comma = 'Comma',
    String = 'String',
    Number = 'Number',
    True = 'True',
    False = 'False',
    Null = 'Null'
}

export type Token = {
    kind: TokenKind;
    value?: string | number | boolean | null;
}

export function lex(input: string): Token[] {
    const tokens: Token[] = [];
    let i = 0;

    while (i < input.length) {
        const char = input[i];

        switch (char) {
            case '{':
                tokens.push({kind: TokenKind.LeftBrace});
                break;
            case '}':
                tokens.push({kind: TokenKind.RightBrace});
                break;
            case '[':
                tokens.push({kind: TokenKind.LeftBracket});
                break;
            case ']':
                tokens.push({kind: TokenKind.RightBracket});
                break;
            case ':':
                tokens.push({kind: TokenKind.Colon});
                break;
            case ',':
                tokens.push({kind: TokenKind.Comma});
                break;
            case '"': {
                let str = '';
                i++;
                while (i < input.length && input[i] !== '"') {
                    str += input[i];
                    i++;
                }
                tokens.push({kind: TokenKind.String, value: str});
                break;
            }
            case '0':
            case '1':
            case '2':
            case '3':
            case '4':
            case '5':
            case '6':
            case '7':
            case '8':
            case '9':
                let numStr = '';
                while (i < input.length && '0123456789'.indexOf(input[i]) >= 0) {
                    numStr += input[i];
                    i++;
                }
                tokens.push({kind: TokenKind.Number, value: parseFloat(numStr)});
                break;
            case 't':
                if (input.slice(i, i + 4) === 'true') {
                    tokens.push({kind: TokenKind.True});
                    i += 3;
                } else {
                    throw new Error(`Unexpected token at position ${i}`);
                }
                break;
            case 'f':
                if (input.slice(i, i + 5) === 'false') {
                    tokens.push({kind: TokenKind.False});
                    i += 4;
                } else {
                    throw new Error(`Unexpected token at position ${i}`);
                }
                break;
            case 'n':
                if (input.slice(i, i + 4) === 'null') {
                    tokens.push({kind: TokenKind.Null});
                    i += 3;
                } else {
                    throw new Error(`Unexpected token at position ${i}`);
                }
                break;
        }

        i++;
    }
    return tokens;
}