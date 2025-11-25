import { lex } from "./lexer.ts";
import { Parser } from "./parser.ts";
import { Formatter } from "./formatter.ts";
import {YmlFormatter} from "./ymlFormatter.ts";

const input = {
  name: "John",
  age: 30,
  isAdmin: true,
  hobbies: ["sports", "music"],
  something: null,
  address: {
    street: "123 Main St",
    city: "New York",
    state: "NY",
  },
};

const inputString = JSON.stringify(input);
const tokens = lex(inputString);

const parser = new Parser(tokens);
const jtoken = parser.parse();

const jsonFormatter = new Formatter({
    casing: "camel",
    minify: false,
    indent: 2,
    includeNull: true
});
// console.log(jsonFormatter.format(jtoken));

const ymlFormatter = new YmlFormatter();
console.log(ymlFormatter.format(jtoken));
