import { Token } from "./lexer.ts";

export type JValue = string | number | boolean | null;
export type JArray = JToken[];
export type JObject = { [key: string]: JToken };
export type JToken = JValue | JObject | JArray;

export class Parser {
  private i = 0;

  constructor(private tokens: Token[]) {}

  public parse(): JToken {
    const token = this.tokens[this.i];
    this.i++;

    if (token.kind === "LeftBrace") {
      return this.parseObject();
    }

    if (token.kind === "LeftBracket") {
      return this.parseArray();
    }

    if (token.kind === "True") {
      return true;
    }
    if (token.kind === "False") {
      return false;
    }
    if (token.kind === "Null") {
      return null;
    }

    return token.value as JToken;
  }

  private parseObject(): JObject {
    const tokens: JObject = {};
    while (this.tokens[this.i].kind !== "RightBrace") {
      const key = this.tokens[this.i].value as string;
      this.i++; // Key
      this.i++; // Colon
      tokens[key] = this.parse(); // Value

      if (this.tokens[this.i].kind === "Comma") {
        this.i++; // Comma
      }
    }

    this.i++; // RightBrace
    return tokens;
  }

  private parseArray(): JArray {
    const tokens: JToken[] = [];

    while (this.tokens[this.i].kind !== "RightBracket") {
      const childToken = this.parse();
      tokens.push(childToken);

      if (this.tokens[this.i].kind === "Comma") {
        this.i++; // Comma
      }
    }

    this.i++; // RightBracket
    return tokens;
  }
}
