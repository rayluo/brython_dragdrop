__version__ = "0.1.0"
# Other drag-and-drop ideas: https://smart-interface-design-patterns.com/articles/drag-and-drop-ux/


try:
    from browser import document
except ModuleNotFoundError:
    print("Warning: This package is designed for Brython only.")

class DraggableMixin(object):
    """To be mixed with an html tag, such as html.SPAN"""
    def __init__(self, *args, **kwargs):
        #kwargs.setdefault("id", "id_{}".format(id(self)))
        if not kwargs.get("id"):
            kwargs["id"] = "id_{}".format(id(self))
        if not kwargs.get("Class"):
            kwargs["Class"] = self.__class__.__name__
        kwargs["draggable"] = True
        super(DraggableMixin, self).__init__(*args, **kwargs)
        self.bind("mouseover", self.__mouseover)
        self.bind("dragstart", self.__dragstart)

    @staticmethod
    def __mouseover(event):
        event.target.style.cursor = "pointer"

    @staticmethod
    def __dragstart(event):
        event.dataTransfer.setData("dragged", event.target.id)  # data has to be a string


def swap(dragged: DraggableMixin, target: DraggableMixin):
    """This is a rule action to swap dragged object and target"""
    assert isinstance(target, DraggableMixin)
    # Swapping arbitrary elements, learn from https://stackoverflow.com/a/10717422
    temp = document.createElement("SPAN")
    dragged.parentNode.insertBefore(temp, dragged)
    target.parentNode.insertBefore(dragged, target)
    temp.parentNode.insertBefore(target, temp)
    temp.parentNode.removeChild(temp)


def join(dragged: DraggableMixin, target):
    """This is a rule action to join/append dragged object to target container.

    So the landing container may contain more and more dragged objects"""
    assert not isinstance(target, DraggableMixin)
    target.appendChild(dragged)  # This also seems to work: target.attach(dragged)


def occupy(dragged: DraggableMixin, target):
    """This is a rule action to occupy target with dragged object.

    Existing occupants - if any - will be swapped out."""
    assert not isinstance(target, DraggableMixin)
    occupants = target.select('[draggable="true"]')
    if len(occupants) > 1:
        print("We haven't implemented swapping multiple occupants, yet")
    elif len(occupants) == 1:
        swap(dragged, occupants[0])
    else:  # The target is empty
        target.appendChild(dragged)


def make_droppable(selector, rules=None):
    """Makes document.select(selector) elements droppable.

    :param string selector: A CSS selector to match some html elements.

    :param dict rules:
        Since Python 3.7, dict has order. Define high priority rule first.
        Usage: (SubClassOfDraggableMixin, SubClassOfDraggableMixin): Action
        where actions are: swap, occupy, join.
    """
    engine = _RulesEngine(rules)
    for element in document.select(selector):
        element.bind("dragover", engine._dragover)
        element.bind("drop", engine._drop)


class _RulesEngine(object):  # Will make it public when we see a need to subclass it
    def __init__(self, rules):
        self._rules = rules or {
            (DraggableMixin, DraggableMixin): swap,  # Note that
                # draggable elements inside a droppable area is also droppable,
                # therefore we also need to define action for them
            (DraggableMixin, object): join,  # object matches any html element (which was chosen by selector)
        }

    def _dragover(self, event):
        dragged = document[event.dataTransfer.getData("dragged")]
        if self.is_droppable(dragged, event.target):
            event.dataTransfer.dropEffect = "move"
            event.preventDefault()

    def is_droppable(self, dragged, target):
        """Decides whether the dragged element is actually droppable on target.

        The default implementation looks up the rules.
        You may override it.
        """
        return self._choose_rule(dragged, target) is not None

    def _choose_rule(self, dragged, target):
        for d, t in self._rules:
            if isinstance(dragged, d) and isinstance(target, t):
                return self._rules[(d, t)]

    def _drop(self, event):
        dragged = document[event.dataTransfer.getData("dragged")]
        target = event.target  # Note that the target may be a droppable element,
            # or an draggable element that was previously dropped into the element.
        self._choose_rule(dragged, target)(dragged, target)
        event.preventDefault()
        self.on_dropped(dragged, target)

    def on_dropped(self, dragged, target):
        """You can subclass and change this to add your post-drag logic"""

