#!/usr/bin/env python

import sys

if len(sys.argv) != 2:
  print "Usage: " + sys.argv[0] + " <location_of_SMRX.vtk>"
  sys.exit()

import vtk

radius = 20
num_points = 100
prop_time = 500
tube_radius = .5
step_len = .1

ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

reader = vtk.vtkDataSetReader()
reader.SetFileName(sys.argv[1])
reader.Update()

contour = vtk.vtkContourFilter()
contour.SetInputConnection(reader.GetOutputPort())
contour.SetValue(0, 9)

contourMapper = vtk.vtkPolyDataMapper()
contourMapper.SetInputConnection(contour.GetOutputPort())
contourMapper.ScalarVisibilityOff() # do not colour by scalar values ...

contourActor = vtk.vtkActor()
contourActor.SetMapper(contourMapper)
contourActor.GetProperty().SetColor(.9,.9,.9) # ... use this colour
contourActor.GetProperty().SetOpacity(.7) 
ren.AddActor(contourActor)

dims = reader.GetOutput().GetExtent()
cy = (dims[3] - dims[2]) / 4.0
cz = (dims[5] - dims[4]) / 2.0

particle_source = vtk.vtkPointSource()
particle_source.SetCenter(0, cy, cz)
particle_source.SetRadius(radius)
particle_source.SetNumberOfPoints(num_points)

stream_lines = vtk.vtkStreamLine()
stream_lines.SetInputConnection(reader.GetOutputPort())
stream_lines.SetSourceConnection(particle_source.GetOutputPort())
stream_lines.SetStepLength(step_len)
stream_lines.SetMaximumPropagationTime(prop_time)
stream_lines.SetTerminalSpeed(0.05)
stream_lines.SetIntegrationDirectionToForward()

tube_filter = vtk.vtkTubeFilter()
tube_filter.SetInputConnection(stream_lines.GetOutputPort())
tube_filter.SetRadius(tube_radius)

tube_mapper = vtk.vtkPolyDataMapper()
tube_mapper.SetInputConnection(tube_filter.GetOutputPort())
tube_mapper.ScalarVisibilityOff()

tube_actor = vtk.vtkActor()
tube_actor.SetMapper(tube_mapper)
tube_actor.GetProperty().SetColor(1,0.5,0.5)
ren.AddActor(tube_actor)

particle_source2 = vtk.vtkPointSource()
particle_source2.SetCenter(0, cy*3, cz)
particle_source2.SetRadius(radius)
particle_source2.SetNumberOfPoints(num_points)

stream_lines2 = vtk.vtkStreamLine()
stream_lines2.SetInputConnection(reader.GetOutputPort())
stream_lines2.SetSourceConnection(particle_source2.GetOutputPort())
stream_lines2.SetStepLength(step_len)
stream_lines2.SetMaximumPropagationTime(prop_time)
stream_lines2.SetTerminalSpeed(0.05)
stream_lines2.SetIntegrationDirectionToForward()

tube_filter2 = vtk.vtkTubeFilter()
tube_filter2.SetInputConnection(stream_lines2.GetOutputPort())
tube_filter2.SetRadius(tube_radius)

tube_mapper2 = vtk.vtkPolyDataMapper()
tube_mapper2.SetInputConnection(tube_filter2.GetOutputPort())
tube_mapper2.ScalarVisibilityOff()

tube_actor2 = vtk.vtkActor()
tube_actor2.SetMapper(tube_mapper2)
tube_actor2.GetProperty().SetColor(0,1,0)

ren.AddActor(tube_actor2)

outline = vtk.vtkOutlineFilter()
outline.SetInputConnection(reader.GetOutputPort())

outline_mapper = vtk.vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtk.vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(0.9, 0.9, 0.9)

ren.AddActor(outline_actor)



ren.GradientBackgroundOn()
ren.SetBackground(.32,.58,.92)
ren.SetBackground2(.6,.8,.92)

renWin.SetSize(640,480)
iren.Initialize()
iren.Start()