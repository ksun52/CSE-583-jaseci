
enum Color;
:enum:Color {
    RED = 1,
    GREEN = 2
}

can uses_enum {
    print(Color.RED.value);
}

with entry {
    uses_enum();
}