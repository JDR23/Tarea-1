
from __future__ import annotations
import argparse
from pathlib import Path
from library import Library, JSONStorage

DB_PATH = Path("data/db.json")

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Gestor de biblioteca (POO) con almacenamiento JSON simple."
    )
    sub = p.add_subparsers(dest="command", required=True)

    # add-book
    p_addb = sub.add_parser("add-book", help="Agregar un libro nuevo")
    p_addb.add_argument("--title", required=True)
    p_addb.add_argument("--author", required=True)

    # list-books
    sub.add_parser("list-books", help="Listar todos los libros")

    # add-member
    p_addm = sub.add_parser("add-member", help="Agregar un miembro")
    p_addm.add_argument("--name", required=True)

    # list-members
    sub.add_parser("list-members", help="Listar todos los miembros")

    # borrow
    p_borrow = sub.add_parser("borrow", help="Prestar un libro a un miembro")
    p_borrow.add_argument("--member-id", type=int, required=True)
    p_borrow.add_argument("--book-id", type=int, required=True)

    # return
    p_return = sub.add_parser("return", help="Devolver un libro")
    p_return.add_argument("--book-id", type=int, required=True)

    return p

def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    lib = Library(JSONStorage(DB_PATH))

    if args.command == "add-book":
        book = lib.add_book(args.title, args.author)
        print(f"Libro agregado: #{book.id} - {book.title} ({book.author})")
    elif args.command == "list-books":
        for b in lib.list_books():
            estado = "prestado" if b.is_borrowed else "disponible"
            print(f"#{b.id} - {b.title} ({b.author}) -> {estado}")
    elif args.command == "add-member":
        m = lib.add_member(args.name)
        print(f"Miembro agregado: #{m.id} - {m.name}")
    elif args.command == "list-members":
        for m in lib.list_members():
            estado = "activo" if m.active else "inactivo"
            print(f"#{m.id} - {m.name} -> {estado}")
    elif args.command == "borrow":
        lib.borrow_book(args.member_id, args.book_id)
        print(f"Libro #{args.book_id} prestado al miembro #{args.member_id}.")
    elif args.command == "return":
        lib.return_book(args.book_id)
        print(f"Libro #{args.book_id} devuelto.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
