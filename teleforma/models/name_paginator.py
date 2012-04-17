import string
from django.core.paginator import InvalidPage, EmptyPage

class NamePaginator(object):
    """Pagination for string-based objects"""
    
    def __init__(self, object_list, on=None, per_page=25):
        self.object_list = object_list
        self.count = len(object_list)
        self.pages = []
        
        # chunk up the objects so we don't need to iterate over the whole list for each letter
        chunks = {}
        
        for obj in self.object_list:
            if on: obj_str = str(getattr(obj, on))
            else: obj_str = str(obj)
            
            letter = str.upper(obj_str[0])
            
            if letter not in chunks: chunks[letter] = []
            
            chunks[letter].append(obj)
        
        # the process for assigning objects to each page
        current_page = NamePage(self)
        
        for letter in string.ascii_uppercase:
            if letter not in chunks: 
                current_page.add([], letter)
                continue
            
            sub_list = chunks[letter] # the items in object_list starting with this letter
            
            new_page_count = len(sub_list) + current_page.count
            # first, check to see if sub_list will fit or it needs to go onto a new page.
            # if assigning this list will cause the page to overflow...
            # and an underflow is closer to per_page than an overflow...
            # and the page isn't empty (which means len(sub_list) > per_page)...
            if new_page_count > per_page and \
                    abs(per_page - current_page.count) < abs(per_page - new_page_count) and \
                    current_page.count > 0:
                # make a new page
                self.pages.append(current_page)
                current_page = NamePage(self)
            
            current_page.add(sub_list, letter)
        
        # if we finished the for loop with a page that isn't empty, add it
        if current_page.count > 0: self.pages.append(current_page)
        
    def page(self, num):
        """Returns a Page object for the given 1-based page number."""
        if len(self.pages) == 0:
            return None
        elif num > 0 and num <= len(self.pages):
            return self.pages[num-1]
        else:
            raise InvalidPage
    
    @property
    def num_pages(self):
        """Returns the total number of pages"""
        return len(self.pages)

class NamePage(object):
    def __init__(self, paginator):
        self.paginator = paginator
        self.object_list = []
        self.letters = []
    
    @property
    def count(self):
        return len(self.object_list)
    
    @property
    def start_letter(self):
        if len(self.letters) > 0: 
            self.letters.sort(key=str.upper)
            return self.letters[0]
        else: return None
    
    @property
    def end_letter(self):
        if len(self.letters) > 0: 
            self.letters.sort(key=str.upper)
            return self.letters[-1]
        else: return None
    
    @property
    def number(self):
        return self.paginator.pages.index(self) + 1
    
    def add(self, new_list, letter=None):
        if len(new_list) > 0: self.object_list = self.object_list + new_list
        if letter: self.letters.append(letter)
    
    def __repr__(self):
        if self.start_letter == self.end_letter:
            return self.start_letter
        else:
            return '%c-%c' % (self.start_letter, self.end_letter)