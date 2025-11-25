import type { JArray, JObject, JToken, JValue } from "./parser.ts";

export interface FormatterOptions {
  indent: number;
  minify: boolean;
  casing: "camel" | "pascal";
  includeNull: boolean;
}

export class Formatter {
  private level = 0;
  constructor(private options: FormatterOptions) {}

  format(token: JToken): string | null {
    if (token === undefined) {
      throw new Error("Token is undefined");
    }
    if (token === null) {
      return this.options.includeNull ? "null" : null;
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
    const separationChar = this.options.minify ? "," : ",\n";
    const indent = this.ident();

    this.level++;
    const body = Object.getOwnPropertyNames(obj)
      .reduce((acc, key) => {
        const value = obj[key];
        const keyCased = this.options.casing === "camel"
          ? key.charAt(0).toLowerCase() + key.slice(1)
          : key.charAt(0).toUpperCase() + key.slice(1);
        const formattedValue = this.format(value);
        if (formattedValue !== null) {
          acc.push(`${this.ident()}"${keyCased}":${formattedValue}`);
        }
        return acc;
      }, [] as string[])
      .join(separationChar);
    this.level--;
    if (this.options.minify) {
      return `{${body}}`;
    }

    return `{\n${body}\n${indent}}`;
  }

  private formatArray(array: JArray): string {
    const separationChar = this.options.minify ? "," : ",\n";
    const indent = this.ident();

    this.level++;
    const body = array
      .reduce(
        (acc, child) => {
          const value = this.format(child);
          if (value !== null) {
            acc.push(`${this.ident()}${value}`);
          }

          return acc;
        },
        [] as string[],
      )
      .join(separationChar);

    this.level--;
    if (this.options.minify) {
      return `[${body}]`;
    }

    return `[\n${body}\n${indent}]`;
  }

  private formatValue(value: JValue): string {
    if (value === true) {
      return "true";
    }
    if (value === false) {
      return "false";
    }
    if (typeof value === "string") {
      return `"${value}"`;
    }
    if (typeof value === "number") {
      return value.toString();
    }
    throw new Error(`Invalid value type ${value}`);
  }

  private ident() {
    return !this.options.minify
      ? " ".repeat(this.options.indent * this.level)
      : "";
  }
}
