class LibraryItem:

    def __init__(self, _library_item_id, _title):
        self._library_item_id = _library_item_id
        self._title = _title
        self._location = "ON_SHELF"
        self._checked_out_by = None
        self._requested_by = None
        self._date_checked_out = 0

    def get_library_item_id(self):
        """
        get the id of the library item
        :return: libray_item_id
        """
        return self._library_item_id

    def get_title(self):
        """
        get the title of the library item
        :return: title
        """
        return self._title

    def get_location(self):
        """
        get the location of the library item
        :return: location
        """
        return self._location

    def get_checked_out_by(self):
        """
        get checked_out_by attribute of the class
        :return: checked_out_by
        """
        return self._checked_out_by

    def get_requested_by(self):
        """
        get requested_by attribute of the class
        :return: requested_by
        """
        return self._requested_by

    def get_date_checked_out(self):
        return self._date_checked_out

    def set_date_checked_out(self, current_date):
        self._date_checked_out = current_date

    def set_location(self, new_location):
        self._location = new_location

    def set_library_item_id(self, library_item):
        self._library_item_id = library_item

    def set_checked_out_by(self, patron):
        self._checked_out_by = patron

    def set_requested_by(self, patron):
        self._requested_by = patron



class Book(LibraryItem):
    def __init__(self, _library_item_id, _title, _author):
        self._author = _author
        self._date_checked_out = None
        super().__init__(_library_item_id, _title)

    def get_check_out_length(self):
        return 21

    def author(self):
        return self._author



class Album(LibraryItem):
    def __init__(self, _library_item_id, _title, _artist):
        self._artist = _artist
        self._date_checked_out = None
        super().__init__(_library_item_id, _title)

    def get_check_out_length(self):
        return 14

    def get_artist(self):
        return self._artist



class Movie(LibraryItem):
    def __init__(self, _library_item_id, _title, _director):
        self._director = _director
        self._date_checked_out = None
        super().__init__(_library_item_id, _title)

    def get_check_out_length(self):
        return 7

    def get_director(self):
        return self._director


class Patron:
    def __init__(self, _patron_id, _name):
        self._patron_id = _patron_id
        self._name = _name
        self._checked_out_items = []
        self._fine_amount = 0

    def get_fine_amount(self):
        return self._fine_amount

    def get_patron_id(self):
        return self._patron_id

    def get_name(self):
        return self._name

    def get_checked_out_items(self):
        return self._checked_out_items

    def add_library_item(self, library_item):
        self._checked_out_items.append(library_item)

    def remove_library_item(self, library_item):
        for item in self._checked_out_items:
            if item == library_item:
                self._checked_out_items.remove(item)

    def amend_fine(self, fine):
        self._fine_amount += fine



class Library:
    def __init__(self):
        self._current_date = 0
        self._holdings = []
        self._members = []

    def get_current_date(self):
        return self._current_date

    def add_library_item(self, library_item):
        self._holdings.append(library_item)

    def add_patron(self, patron):
        self._members.append(patron)

    def lookup_library_item_from_id(self, item_id):
        found = False
        for library_items in self._holdings:
            if item_id == library_items.get_library_item_id():
                found = True
                return library_items
        if not found:
            return None

    def lookup_patron_from_id(self, member_id):
        found = False
        for people in self._members:
            if member_id == people.get_patron_id():
                found = True
                return people
        if not found:
            return None

    def check_out_library_item(self, patron_id, library_item_id):
        patron = self.lookup_patron_from_id(patron_id)
        library_item = self.lookup_library_item_from_id(library_item_id)

        if patron_id == patron.get_patron_id():
            if library_item_id == library_item.get_library_item_id():
                if library_item.get_checked_out_by() is None:
                    if patron == library_item.get_requested_by():
                        library_item.set_checked_out_by(patron)
                        library_item.set_date_checked_out(self._current_date)
                        library_item.set_location("CHECKED_OUT")

                        if library_item.get_requested_by() == patron:
                            library_item.set_requested_by(None)
                            patron.add_library_item(library_item)
                            print("check out successful")

                    else:
                        return "item on hold by other patron"
                else:
                    return "item already checked out"
            else:
                return "item not found"
        else:
            return "patron not found"

    def return_library_item(self, library_item_id):
        library_item = self.lookup_library_item_from_id(library_item_id)
        patron = library_item.get_checked_out_by()

        if library_item_id == library_item.get_library_item_id():

            if library_item.get_checked_out_by() is not None:
                patron.remove_library_item(library_item)

                if library_item.get_requested_by() is not None:
                    library_item.set_location("ON_HOLD_SHELF")
                    print("return successful")

                else:
                    library_item.set_location("ON_SHELF")
                    print("return successful")

            else:
                return "item already in library"

        else:
            return "item not found"

    def request_library_item(self, patron_id, library_item_id):
        patron = self.lookup_patron_from_id(patron_id)
        library_item = self.lookup_library_item_from_id(library_item_id)

        if patron is not None and patron_id == patron.get_patron_id():

            if library_item_id == library_item.get_library_item_id():

                if library_item.get_requested_by() is None:
                    library_item.set_requested_by(patron)

                    if library_item.get_location() == "ON_SHELF":
                        library_item.set_location("ON_HOLD_SHELF")

                    print("request successful")

                else:
                    return "item already on hold"
            else:
                return "item not found"
        else:
            return "patron not found"

    def pay_fine(self, patron_id, cost):
        patron = self.lookup_patron_from_id(patron_id)
        if patron_id == patron.get_patron_id():
            patron.amend_fine(cost)
            print("payment successful")
        else:
            print("patron not found")

    def increment_current_date(self):
        """
        Increase the current date for library
        :return: none
        """
        self._current_date += 1
        for patron in self._members:
            for item in patron.get_checked_out_items():
                if (int(self._current_date) - int(item.get_date_checked_out())) > item.get_check_out_length():
                    patron.amend_fine(0.10)