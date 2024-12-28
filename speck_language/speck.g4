grammar speck;

start: statement*;

statement:
    loop_statement
    | conditional_statement
    | assigment_statement
    | input_statement
    | output_statement ;

loop_statement: 'while' '(' expression ')' program_block;

conditional_statement: 'if' '(' expression ')' program_block;

expression:
    VariableName
    | ConstantName
    | NumberLiteral
    | expression ('==' | '!=' | '>' | '<' | '>=' | '<=' ) expression
    | '(' expression ')'
    | expression ('*' | '/' | '%') expression
    | expression ('+' | '-') expression
    | '!' expression
    | expression ('and' | 'or') expression;

assigment_statement:
    variable_assigment
    | constant_assigment ;

input_statement: 'in(' (VariableName | ConstantName) ')' end_of_statement;

output_statement: 'out(' expression ')' end_of_statement;

program_block: '{' statement* '}';

variable_assigment: VariableName '=' expression end_of_statement ;

constant_assigment: ConstantName '=' expression end_of_statement;

end_of_statement: ';';

VariableName: [a-z][a-zA-Z_0-9]* ;
ConstantName: [A-Z][a-zA-Z_0-9]* ;
NumberLiteral: [-]?[0-9]+ ('.'[0-9]+)?;
WS: [ \t\n\r]+ -> skip;