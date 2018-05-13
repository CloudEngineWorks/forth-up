tests = [
  ['2 3 +', [5]],
  ['5 2 *', [10]],
  ['6 dup *', [36]],
  ['0 [ 6 2 * ] 42 if-else', [42]],
  ['1 [ 6 2 * ] 42 if-else', [12]],
  ['1 [ 2 0 [ 3 3 * ] [ 2 1 + ] if-else 7 * + ] if', [23]],
  ['1 [ 2.5 0 [ 3 2.999 * ] [ 2 1 + ] if-else 7.01 * + ] if', [23.53]],
  ['1 1 if', [1]],
  ['0 0 if', []],
  ['10 count-down', [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]],
  ['3 count-down', [3, 2, 1]],
  ['1 count-down', [1]],
  ['5 fact', [120]],
  ['a 1 2 3 4 n*', ["a", 24]],
  ['"hello world" 1 2 3 4 n*', ["hello world", 24]],
  ['"hello world 5 o\'clock" 1 2 3 4 n*', ["hello world 5 o'clock", 24]],
  ["'hello world 5\" of rain' 4 count-down n*", ['hello world 5" of rain', 24]],
  ["'hello world 5\" of rain' 4 count-down n* 'hello world 5\" of rain'", ['hello world 5" of rain', 24, 'hello world 5" of rain']],
  ['"clock" 1 2 3 4 n*', ["clock", 24]],
  ['{ a: 2 b: 3 }', [{"a":2, "b":3}]],
  ['{ a: 2 b: 4 } a get swap b get swap drop', [2, 4]],
  ['1 { a: 2 b: 4 } a get 3 * swap b get swap drop', [1, 6, 4]],
  ["1 { a: 'hello world' b: 4 } a get swap b get swap drop", [1, 'hello world', 4]],
  ['1 { a: "hello world" b: 4 } a get swap b get swap drop', [1, "hello world", 4]],
  ["5 { a: 'hello' b: 'world' } a get swap b get swap drop", [5, 'hello', 'world']],
  ['5 { a: "hello" b: "world" } a get swap b get swap drop', [5, "hello", "world"]],
  ['1 { a: 2 b: 4 } a get 3 * swap b get swap drop', [1, 6, 4]],
  ['1 { a: 2 b: 4 } a get 3 * swap b get swap drop', [1, 6, 4]]
]