num_books = num_libraries = num_days = 0
books_stock = {} # key: book_id, val: set of libraries
books = [] # list to store the books (id is index)
libraries = [] # list to store the libraries (where id is the index)

###############################################################################
"""                                  Class                                  """
###############################################################################

class Book():

    def __init__(self, book_id, score):
        self.book_id = book_id
        self.score = score
        self.shipped = False

    def __repr__(self):
        return f'<Book book_id={self.book_id} score={self.score} shipped={self.shipped}>'

    def ship_book(self):
        self.shipped = True


class Library():

    def __init__(self, library_id, num_books, signup_days, shipments_per_day, library_books):
        self.library_id = library_id
        self.num_books = num_books
        self.books_not_visited = num_books
        self.signup_days = signup_days
        self.shipments_per_day = shipments_per_day
        self.library_books = sorted(library_books, key=(lambda book_id: books[book_id].score), reverse=True)
        self.total_score = sum([books[book_id].score for book_id in library_books])
        self.score_not_visited = sum([books[book_id].score for book_id in library_books])

    def __repr__(self):
        return f'<Library library_id={self.library_id} num_books={self.num_books} signup_days={self.signup_days} shipments_per_day={self.shipments_per_day} books={self.library_books} total_score={self.total_score} >'

    def get_priority(self, days_left):
        days_to_scan = days_left - self.signup_days
        num_books_to_scan = days_to_scan * self.shipments_per_day
        total_score = 0
        for book_id in self.library_books[:num_books_to_scan]:
            total_score += books[book_id].score
        return total_score

    def score_of_last(self, days, lib_id):
        num_books_to_scan = days * self.shipments_per_day
        books_minus_dupes = list(set(self.library_books) - set(libraries[lib_id].library_books))
        total_score = 0
        for book_id in books_minus_dupes[-num_books_to_scan:]:
            total_score += books[book_id].score
        return total_score

###############################################################################
"""                                  Setup                                  """
###############################################################################

output_file = open("f_solution.txt", "w+")
input_file = 'f_libraries_of_the_world.txt'
with open(input_file) as fp:
    line = fp.readline()
    num_books, num_libraries, num_days = [int(x) for x in line.strip().split()]

    line = fp.readline()
    books_arr = [int(x) for x in line.strip().split()]
    for i in range(num_books):
        books_stock[i] = set()
        books.append(
            Book(
                book_id=i,
                score=books_arr[i]
            )
        )

    line = fp.readline()
    while line:
        library_arr = [int(x) for x in line.strip().split()]
        if len(library_arr) == 0:
            line = fp.readline()
            continue
        line = fp.readline()
        book_arr = [int(x) for x in line.strip().split()]
        for book_id in book_arr:
            books_stock[book_id].add(len(libraries))

        libraries.append(
            Library(
                library_id=len(libraries),
                num_books=library_arr[0],
                signup_days=library_arr[1],
                shipments_per_day=library_arr[2],
                library_books=book_arr
            )
        )

        line = fp.readline()

###############################################################################
"""                             Helper Functions                             """
###############################################################################


###############################################################################
"""                                  Check                                  """
###############################################################################

sol_num_libraries = 0
sol_library_order = []

days_left = num_days

libraries_visited = set()
books_shipped = set()
# curr_day = 0
while days_left > 0:
    max_lib_ind = -1
    max_lib_score = 0
    for i in range(len(libraries)):
        if i in libraries_visited:
            continue
        lib_score = libraries[i].get_priority(days_left)
        max_penalty = 0
        for j in range(len(libraries)):
            if i != j:
                curr_penalty = libraries[j].score_of_last(libraries[i].signup_days, i)
                max_penalty = max(max_penalty, curr_penalty)
        lib_score -= max_penalty
        if lib_score > max_lib_score:
            max_lib_score = lib_score
            max_lib_ind = i
    if max_lib_ind == -1:
        break
    # we've found the library
    days_left -= libraries[max_lib_ind].signup_days
    lib_books_shipped = []
    shipped_days = 0
    # add the books it wants shipped to the solution
    books_minus_dupes = sorted(list(set(libraries[max_lib_ind].library_books) - set(books_shipped)), key=(lambda book_id: books[book_id].score), reverse=True)
    num_books_to_ship = days_left * libraries[max_lib_ind].shipments_per_day
    lib_books_shipped = books_minus_dupes[:num_books_to_ship]
    books_shipped |= set(books_minus_dupes[:num_books_to_ship])
    sol_library_order.append((max_lib_ind, lib_books_shipped))
    sol_num_libraries += 1
    libraries_visited.add(max_lib_ind)
        
        
###############################################################################
"""                                 Solution                                """
###############################################################################

output_file.write(f'{sol_num_libraries}\n')
sol_library_order_str =""
for lib in sol_library_order:
    sol_library_order_str += str(lib[0]) + " " + str(len(lib[1])) + "\n"
    # print(lib)
    sol_library_order_str += ' '.join(str(book_id) for book_id in lib[1]) + '\n'
output_file.write(f'{sol_library_order_str}\n')
