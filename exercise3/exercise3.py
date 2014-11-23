#!/usr/bin/env python

import sys

if len(sys.argv) != 2:
  print "Usage: " + sys.argv[0] + " <location_of_SMRX.vtk>"
  sys.exit()

import vtk

radius = 20
num_points = 200
prop_time = 500
step_len = .1

#	Read in the dataset
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

reader = vtk.vtkDataSetReader()
reader.SetFileName(sys.argv[1])
reader.Update()


#	Geometry of the reactor
contour = vtk.vtkContourFilter()
contour.SetInputConnection(reader.GetOutputPort())
contour.SetValue(0, 10)

contour_mapper = vtk.vtkPolyDataMapper()
contour_mapper.SetInputConnection(contour.GetOutputPort())
contour_mapper.ScalarVisibilityOff()

contour_actor = vtk.vtkActor()
contour_actor.SetMapper(contour_mapper)
contour_actor.GetProperty().SetColor(.9,.9,.9)
ren.AddActor(contour_actor)


#	Calculating starting point of particles
dims = reader.GetOutput().GetExtent()
cy = (dims[3] - dims[2]) / 4.0
cz = (dims[5] - dims[4]) / 2.0


#	Creation of patricle source 1
particle_source = vtk.vtkPointSource()
particle_source.SetCenter(0, cy, cz)
particle_source.SetRadius(radius)
particle_source.SetNumberOfPoints(num_points)

#	Add streamlines from pointsource
stream_lines = vtk.vtkStreamLine()
stream_lines.SetInputConnection(reader.GetOutputPort())
stream_lines.SetSourceConnection(particle_source.GetOutputPort())
stream_lines.SetStepLength(step_len)
stream_lines.SetMaximumPropagationTime(prop_time)
stream_lines.SetTerminalSpeed(0.05)
stream_lines.SetIntegrationDirectionToForward()

#	Add tube around streamlines
tube_filter = vtk.vtkTubeFilter()
tube_filter.SetInputConnection(stream_lines.GetOutputPort())
tube_filter.SetVaryRadiusToVaryRadiusByVector()
tube_filter.CappingOn()
tube_filter.SetNumberOfSides(10)

#	Map data, set coloring through scalar off
tube_mapper = vtk.vtkPolyDataMapper()
tube_mapper.SetInputConnection(tube_filter.GetOutputPort())
tube_mapper.ScalarVisibilityOff()

#	Add actor to set color to blue
tube_actor = vtk.vtkActor()
tube_actor.SetMapper(tube_mapper)
tube_actor.GetProperty().SetColor(0.3,0.3,1)
ren.AddActor(tube_actor)

#	Creation of patricle source 2
particle_source2 = vtk.vtkPointSource()
particle_source2.SetCenter(0, cy*3, cz)
particle_source2.SetRadius(radius)
particle_source2.SetNumberOfPoints(num_points)

#	Add streamlines from pointsource
stream_lines2 = vtk.vtkStreamLine()
stream_lines2.SetInputConnection(reader.GetOutputPort())
stream_lines2.SetSourceConnection(particle_source2.GetOutputPort())
stream_lines2.SetStepLength(step_len)
stream_lines2.SetMaximumPropagationTime(prop_time)
stream_lines2.SetTerminalSpeed(0.05)
stream_lines2.SetIntegrationDirectionToForward()

#	Add tube around streamlines
tube_filter2 = vtk.vtkTubeFilter()
tube_filter2.SetInputConnection(stream_lines2.GetOutputPort())
tube_filter2.SetVaryRadiusToVaryRadiusByVector()
tube_filter2.CappingOn()
tube_filter2.SetNumberOfSides(10)

#	Map data, set coloring through scalar off
tube_mapper2 = vtk.vtkPolyDataMapper()
tube_mapper2.SetInputConnection(tube_filter2.GetOutputPort())
tube_mapper2.ScalarVisibilityOff()

#	Add actor to set color to red
tube_actor2 = vtk.vtkActor()
tube_actor2.SetMapper(tube_mapper2)
tube_actor2.GetProperty().SetColor(1,0.3,0.3)
ren.AddActor(tube_actor2)

#	Add outline to give orientation
outline = vtk.vtkOutlineFilter()
outline.SetInputConnection(reader.GetOutputPort())

outline_mapper = vtk.vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtk.vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(0.9, 0.9, 0.9)

ren.AddActor(outline_actor)

#	Set a gradient background
ren.GradientBackgroundOn()
ren.SetBackground(.32,.58,.92)
ren.SetBackground2(.6,.8,.92)


#	Set window size
renWin.SetSize(640,480)

#	Start visualization
iren.Initialize()
iren.Start()