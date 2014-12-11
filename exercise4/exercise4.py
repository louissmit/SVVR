from __future__ import division
import sys

if len(sys.argv) != 2:
  print "Usage: " + sys.argv[0] + " <Folder to frog(Tissue).***.raw>"
  sys.exit()

import vtk

frog_dir = sys.argv[1]

ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

frog_reader = vtk.vtkImageReader() 
frog_reader.SetFilePrefix(frog_dir + 'frog.')
frog_reader.SetFilePattern('%s%03d.raw')
frog_reader.SetDataScalarTypeToUnsignedChar()
frog_reader.SetFileDimensionality(2)
frog_reader.SetDataSpacing(1,1,1.5)
frog_reader.SetDataExtent(0,499,0,469,1,136)
frog_reader.Update()


frog_contour = vtk.vtkContourFilter()
frog_contour.SetInputConnection(frog_reader.GetOutputPort())
frog_contour.SetValue(0,10)

frog_mapper = vtk.vtkPolyDataMapper()
frog_mapper.SetInputConnection(frog_contour.GetOutputPort())

frog_actor = vtk.vtkActor()
frog_actor.SetMapper(frog_mapper)
frog_actor.GetProperty().SetOpacity(0.1)

ren.AddActor(frog_actor)



tissue_reader = vtk.vtkImageReader() 
tissue_reader.SetFilePrefix(frog_dir + 'frogTissue.')
tissue_reader.SetFilePattern('%s%03d.raw')
tissue_reader.SetDataScalarTypeToUnsignedChar()
tissue_reader.SetFileDimensionality(2)
tissue_reader.SetDataSpacing(1,1,1.5)
tissue_reader.SetDataExtent(0,499,0,469,1,136)
tissue_reader.Update()

compositeFunction = vtk.vtkVolumeRayCastCompositeFunction()
volume_mapper = vtk.vtkVolumeRayCastMapper()
volume_mapper.SetVolumeRayCastFunction(compositeFunction)
volume_mapper.SetInputConnection(tissue_reader.GetOutputPort())

opacityTransferFunction = vtk.vtkPiecewiseFunction()
opacityTransferFunction.AddPoint(0, 0)
opacityTransferFunction.AddPoint(1, .1)
opacityTransferFunction.AddPoint(2, .1)
opacityTransferFunction.AddPoint(3, .1)
opacityTransferFunction.AddPoint(4, .1)
opacityTransferFunction.AddPoint(5, .1)
opacityTransferFunction.AddPoint(6, .1)
opacityTransferFunction.AddPoint(7, .1)
opacityTransferFunction.AddPoint(8, .1)
opacityTransferFunction.AddPoint(9, .1)
opacityTransferFunction.AddPoint(10, .1)
opacityTransferFunction.AddPoint(11, .1)
opacityTransferFunction.AddPoint(12, .1)
opacityTransferFunction.AddPoint(13, 0)
opacityTransferFunction.AddPoint(14, .1)
opacityTransferFunction.AddPoint(15, .1)

colorTransferFunction = vtk.vtkColorTransferFunction()
colorTransferFunction.AddRGBPoint(1 , 216/255,101/255, 79/255)
colorTransferFunction.AddRGBPoint(2 , 250/255,250/255,225/255)
colorTransferFunction.AddRGBPoint(3 , 255/255,253/255,229/255)
colorTransferFunction.AddRGBPoint(4 , 111/255,184/255,210/255)
colorTransferFunction.AddRGBPoint(5 , 194/255,142/255,  0/255)
colorTransferFunction.AddRGBPoint(6 , 206/255,110/255, 84/255)
colorTransferFunction.AddRGBPoint(7 , 183/255,156/255,220/255)
colorTransferFunction.AddRGBPoint(8 , 185/255,102/255, 83/255)
colorTransferFunction.AddRGBPoint(9 , 204/255,168/255,143/255)
colorTransferFunction.AddRGBPoint(10, 221/255,130/255,101/255)
colorTransferFunction.AddRGBPoint(11, 197/255,165/255,145/255)
colorTransferFunction.AddRGBPoint(12, 255/255,234/255, 92/255)
colorTransferFunction.AddRGBPoint(13, 241/255,214/255,145/255)
colorTransferFunction.AddRGBPoint(14, 157/255,108/255,162/255)
colorTransferFunction.AddRGBPoint(15, 216/255,132/255,105/255)

volume_prop= vtk.vtkVolumeProperty()
volume_prop.SetColor(colorTransferFunction)
volume_prop.SetScalarOpacity(opacityTransferFunction)
volume_prop.SetInterpolationTypeToLinear()


volume = vtk.vtkVolume()
volume.SetMapper(volume_mapper)
volume.SetProperty(volume_prop)

ren.AddVolume(volume)

#	Set a gradient background
ren.GradientBackgroundOn()
ren.SetBackground(.32,.58,.92)
ren.SetBackground2(.6,.8,.92)


#	Set window size
renWin.SetSize(640,480)

#	Start visualization
iren.Initialize()
iren.Start()
