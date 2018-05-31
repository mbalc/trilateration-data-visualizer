# Trilateration Data Visualizer

## Build and install:

To run the program:
- Clone project and enter its main directory
- Either
  - have your environment set to support 'ipython' and 'matplotlib'
  - setup a new venv
    - run `./setup` to deploy a venv
    - each time you want to run the app, first launch `. ./activate` (notice additional spaced out leading dot)
- Run `./run`, wait a while and enjoy!

## Output
Data relevant to the C++ task is printed in console (alongside some additional logging info)
Everything else should show up on a pyplot visualization

## Solution details
- To compute a location of the point we:
  - imagine 'range circles' for each anchor reading
  - take all intersections of each pair of readings relevant to the point 
    - plus, when such circles don't intersect, we take a point that is closest to both circles
    at once)
  - filter out those intersection points that are too far away from a median of these points
  - compute a mean of remaining intersection points
