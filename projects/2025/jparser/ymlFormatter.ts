import type { JArray, JObject, JToken, JValue } from "./parser.ts";

export class YmlFormatter {
  private level = 0;

  format(token: JToken): string | null {
    if (token === undefined) {
      throw new Error("Token is undefined");
    }
    if (token === null) {
      return "null";
    }
    if (Array.isArray(token)) {
      return this.formatArray(token as JArray);
    }
    if (typeof token === "object") {
      return this.formatObject(token as JObject);
    }
    return this.formatValue(token as JValue);
  }

  private formatObject(obj: JObject): string {
    const indent = this.ident();
    this.level++;
    const body = Object.getOwnPropertyNames(obj)
      .reduce((acc, key) => {
        const value = obj[key];
        const formattedValue = this.format(value);
        if (formattedValue !== null) {
          acc.push(`${this.ident()}${key}: ${formattedValue}`);
        }
        return acc;
      }, [] as string[])
      .join("\n");
    this.level--;
    return `\n${body}`;
  }

  private formatArray(array: JArray): string {
    const indent = this.ident();
    this.level++;
    const body = array
      .reduce(
        (acc, child) => {
          const value = this.format(child);
          if (value !== null) {
            acc.push(`${this.ident()}- ${value}`);
          }

          return acc;
        },
        [] as string[],
      )
      .join("\n");

    this.level--;
    return `\n${body}`;
  }

  private formatValue(value: JValue): string {
    if (value === true) {
      return "true";
    }
    if (value === false) {
      return "false";
    }
    if (typeof value === "string") {
        if (value.indexOf(' ') >= 0)
      return `'${value}'`;
        return value;
    }
    if (typeof value === "number") {
      return value.toString();
    }
    throw new Error(`Invalid value type ${value}`);
  }

  private ident() {
    return " ".repeat(2 * this.level);
  }
}
