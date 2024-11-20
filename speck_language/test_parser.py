import sys
from antlr4 import FileStream, CommonTokenStream
from speckLexer import speckLexer
from speckParser import speckParser


def main(input_file, output_file):
    # Załaduj plik wejściowy
    input_stream = FileStream(input_file)

    # Lexer: dzieli tekst na tokeny
    lexer = speckLexer(input_stream)
    token_stream = CommonTokenStream(lexer)

    # Parser: analizuje tokeny na podstawie gramatyki
    parser = speckParser(token_stream)

    # Uruchom parser od reguły startowej
    tree = parser.start()

    # Przygotuj wynik - drzewo składniowe w postaci tekstowej
    tree_str = tree.toStringTree(recog=parser)

    # Zapisz wynik do pliku, dopisując do istniejącej zawartości
    with open(output_file, 'a') as file:
        # Zapisz przykładowy kod wejściowy
        with open(input_file, 'r') as input_f:
            file.write(f"Przykład z pliku: \n{input_f.read()}\n")

        # Zapisz wynik analizy parsera
        file.write(f"Output z analizy: \n{tree_str}\n")
        file.write("="*50 + "\n\n")  # Separator dla kolejnych testów


if __name__ == "__main__":
    # Upewnij się, że podajesz plik wejściowy jako argument
    if len(sys.argv) != 3:
        print("Użycie: python test_parser.py <ścieżka_do_pliku_wejściowego> <ścieżka_do_pliku_wynikowego>")
    else:
        main(sys.argv[1], sys.argv[2])
