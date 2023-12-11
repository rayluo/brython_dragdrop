# Brython.Dragdrop

A library for your Brython apps to implement drag-and-drop UX (User Experience),
without needing to deal with low level drag or drop event callbacks.


## Usage

Here comes some high level description.

1. You create a board game's board using html tags, such as TABLE's TD.

2. You create individual pieces by using normal html tags,
   and then you combine them with `brython_dragdrop.DraggableMixin`. For example:

   ```python
   class Card(brython_dragdrop.DraggableMixin, html.SPAN):
       pass
   ```
   Then create as many cards as you like, and make them visible in your UI.

3. You declare some area to be droppable, by defining rules. For example:

   ```python
   brython_dragdrop.make_droppable(BOARD, rules={
       (Card, Card): brython_dragdrop.swap,
       (Card, html.TD): brython_dragdrop.occupy,
   })
   ```
   Predefined rules include:

   * `swap` which will swap two draggable pieces
   * `join` which will append dragged piece into the landing area,
      so that the landing area may contain more and more dragged pieces.
   * `occupy` which will swap the existing piece (if any) with dragged piece,
      or place dragged piece into the empty landing area.
      So that the landing area will contain up to one draggable piece.

Sample: todo.


## Roadmap

* More sophisticated API to support on-the-spot logic calculation before drop.

