#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 14:05:22 2021

@author: randon
"""
import random

BOTTOMWALL = 0
RIGHTWALL = 1
VISITED = 2
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
DICTOFINAL = []


class Maze:

  def __init__(self,rows,cols, dictofinal=[]):
    
    #INIT 
    self.rows = rows
    self.cols = cols
    
    #??????????
    self.maze = [[[True,True,False] for j in range(cols)] for i in range(rows)]
    
    #START POSITION
    self.startrow = random.randrange(rows)
    self.startcol = random.randrange(cols)
    
    #END POSITION
    self.endrow = random.randrange(rows)
    self.endcol = random.randrange(cols)
    
    #CURR POSITION
    currrow = self.startrow
    currcol = self.startcol

    #GENERATE MAZE WITH CURR POSITION
    self._gen_maze(currrow,currcol)

    #????????????????????????
    self.numtable = [[-1 for j in range(cols)]for i in range(rows)]

    #SOLUTION PATH INIT
    self.solutionpath = []

    
  #-----------------------------------------------------------------------------

  # RETURN ASCII MAZE GRAPHIQUE
  def __str__(self):

    # DEFINE UPPER ROWS
    laby = '.'+self.cols*'_.'+'\n'
    
    # BOUCLE OTHER ROWS
    for i in range(self.rows):
      laby += '|'
      
      # DEFINE WALL
      for j in range(self.cols):
        if self.maze[i][j][BOTTOMWALL]:
          laby += '_'
        else:
          laby += ' '
        if self.maze[i][j][RIGHTWALL]:
          laby += '|'
        else:
          laby += '.'

      laby += '\n'

    laby += 'Start Point   : ('+str(self.startrow)+','+str(self.startcol)+')\n'
    laby += 'End Point     : ('+str(self.endrow)+','+str(self.endcol)+')\n'

    return laby

  #------------------------------------------------------------------------------

  # get a list with posible directions from the current position
  def _get_dirs(self,r,c):
    dirlist = []

    # check limits
    if r-1 >= 0           : dirlist.append(UP)
    if r+1 <= self.rows-1 : dirlist.append(DOWN)
    if c-1 >= 0           : dirlist.append(LEFT)
    if c+1 <= self.cols-1 : dirlist.append(RIGHT)

    return dirlist

  #------------------------------------------------------------------------------

  # generates the maze with depth-first algorithm
  def _gen_maze(self,r,c,d=None):
    maze = self.maze
    # knock down the wall between actual and previous position
    maze[r][c][VISITED] = True
    if   d == UP    : maze[r]  [c]    [BOTTOMWALL] = False
    elif d == DOWN  : maze[r-1][c]    [BOTTOMWALL] = False
    elif d == RIGHT : maze[r]  [c-1]  [RIGHTWALL]  = False
    elif d == LEFT  : maze[r]  [c]    [RIGHTWALL]  = False

    # get the next no visited directions to move
    dirs = self._get_dirs(r,c)
    dicto = []
    # random reorder directions
    for i in range(len(dirs)):
      j = random.randrange(len(dirs))
      dirs[i],dirs[j] = dirs[j],dirs[i]
    
    # make recursive call if the target cell is not visited
    for d in dirs:
      if d==UP:
        if not maze[r-1][c][VISITED]:
          dicto.append((r,c))
          self._gen_maze( r-1,c,UP )
          dicto.append((r-1,c))
          
      elif d==DOWN:
        if not maze[r+1][c][VISITED]:
          dicto.append((r,c))
          self._gen_maze( r+1,c,DOWN )
          dicto.append((r+1,c)) 
          
      if d==RIGHT:  
        if not maze[r][c+1][VISITED]:
          dicto.append((r,c))
          self._gen_maze( r,c+1,RIGHT )
          dicto.append((r,c+1))   
      elif d==LEFT:
        if not maze[r][c-1][VISITED]:
          dicto.append((r,c))
          self._gen_maze( r,c-1,LEFT )
          dicto.append((r,c-1))
      if not dicto == []:
          dictemp=[]
          for i in dicto:
              if i not in dictemp:
                  dictemp.append(i)
          DICTOFINAL.append(dictemp)
    return DICTOFINAL
  #------------------------------------------------------------------------------
  #------ my solver
  def solver(self):
      
      

      
      """
      dictfinal []
      Pour élément dans chaque cellule (r,c):
          dict temp []
          pour direction dans direction liste
              si nord n'a pas de mur et and dans la limite, '
              (r+1,c) append_dict_temp
              
              si sud pas de mur et dans la limite
              (r-1,c) append_dict_temp
              
              si est na pas de mur et dans la limite
              (r,c+1) append dict_temp
              
              si ouest na pas de mur et dans la limite
              (r,c-1) append_dict_temp
              
          dictfinal append dicttemp
          
       transofrmer dictfinal en dictionanire {}
      """
          
  # solve the maze by filling it with numbers(algorithm name?)
  def _solve_maze_aux(self,r,c,n):
    maze = self.maze
    numtable = self.numtable
    numtable[r][c]= n
    # check if the end has been reached
    if (r,c) != (self.endrow,self.endcol):
      directions = self._get_dirs(r,c)

      # recursive calls only if there is no wall between cells and
      # targel cell is not marked (=-1)
      for d in directions:
        if   d==UP    and not maze[r-1][c][BOTTOMWALL] and numtable[r-1][c] == -1:
          self._solve_maze_aux(r-1,c,n+1)
        elif d==DOWN  and not maze[r][c][BOTTOMWALL]   and numtable[r+1][c] == -1:
          self._solve_maze_aux(r+1,c,n+1)
        elif d==RIGHT and not maze[r][c][RIGHTWALL]    and numtable[r][c+1] == -1:
          self._solve_maze_aux(r,c+1,n+1)
        elif d==LEFT  and not maze[r][c-1][RIGHTWALL]  and numtable[r][c-1] == -1:
          self._solve_maze_aux(r,c-1,n+1)
    
  #------------------------------------------------------------------------------

  # get the solution path
  def _get_solution_path(self):
    actrow = self.endrow
    actcol = self.endcol
    startrow = self.startrow
    startcol = self.startcol
    path = []
    numtable = self.numtable
    path = self.solutionpath

    while (actrow,actcol) != (startrow,startcol):
      path.append([actrow,actcol])
      directions = self._get_dirs(actrow,actcol)
      for d in directions:
        if d== UP:
          if numtable[actrow][actcol]-1 == numtable[actrow-1][actcol]:
            actrow -=1
            break
        elif d== DOWN:
          if numtable[actrow][actcol]-1 == numtable[actrow+1][actcol]:
            actrow += 1
            break
        elif d== LEFT:
          if numtable[actrow][actcol]-1 == numtable[actrow][actcol-1]:
            actcol -= 1
            break
        elif d== RIGHT:
          if numtable[actrow][actcol]-1 == numtable[actrow][actcol+1]:
            actcol += 1
            break

    path.append([actrow,actcol])
    path.reverse()
    print("Path :",path)

  #------------------------------------------------------------------------------

  # solve the maze
  def solve_maze(self):
    self._solve_maze_aux(self.startrow,self.startcol,0)
    self._get_solution_path()
 
a =Maze(5,5)
print(a)
print(DICTOFINAL)
