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
frog_contour.ComputeScalarsOff()

frog_mapper = vtk.vtkPolyDataMapper()
frog_mapper.SetInputConnection(frog_contour.GetOutputPort())

frog_actor = vtk.vtkActor()
frog_actor.SetMapper(frog_mapper)
frog_actor.GetProperty().SetOpacity(0.1)
frog_actor.GetProperty().SetColor(0,.5,0)

ren.AddActor(frog_actor)



tissue_reader = vtk.vtkImageReader() 
tissue_reader.SetFilePrefix(frog_dir + 'frogTissue.')
tissue_reader.SetFilePattern('%s%03d.raw')
tissue_reader.SetDataScalarTypeToUnsignedChar()
tissue_reader.SetFileDimensionality(2)
tissue_reader.SetDataSpacing(1,1,1.5)
tissue_reader.SetDataExtent(0,499,0,469,1,136)
tissue_reader.Update()

composite_function = vtk.vtkVolumeRayCastCompositeFunction()
composite_function.SetCompositeMethodToClassifyFirst()
volume_mapper = vtk.vtkVolumeRayCastMapper()
volume_mapper.SetVolumeRayCastFunction(composite_function)
volume_mapper.SetInputConnection(tissue_reader.GetOutputPort())

opacity_transfer_function = vtk.vtkPiecewiseFunction()
opacity_transfer_function.AddPoint(0, 0)
opacity_transfer_function.AddPoint(1, .1)
opacity_transfer_function.AddPoint(2, .1)
opacity_transfer_function.AddPoint(3, .1)
opacity_transfer_function.AddPoint(4, .1)
opacity_transfer_function.AddPoint(5, .1)
opacity_transfer_function.AddPoint(6, .1)
opacity_transfer_function.AddPoint(7, .1)
opacity_transfer_function.AddPoint(8, .1)
opacity_transfer_function.AddPoint(9, .1)
opacity_transfer_function.AddPoint(10, .1)
opacity_transfer_function.AddPoint(11, .1)
opacity_transfer_function.AddPoint(12, .1)
opacity_transfer_function.AddPoint(13, .1)
opacity_transfer_function.AddPoint(14, .1)
opacity_transfer_function.AddPoint(15, .1)
opacity_transfer_function.AddPoint(16, 0)

color_transfer_function = vtk.vtkColorTransferFunction()
color_transfer_function.AddRGBPoint(1 , 216/255,101/255, 79/255)
color_transfer_function.AddRGBPoint(2 , 250/255,250/255,225/255)
color_transfer_function.AddRGBPoint(3 , 255/255,253/255,229/255)
color_transfer_function.AddRGBPoint(4 , 111/255,184/255,210/255)
color_transfer_function.AddRGBPoint(5 , 194/255,142/255,  0/255)
color_transfer_function.AddRGBPoint(6 , 206/255,110/255, 84/255)
color_transfer_function.AddRGBPoint(7 , 183/255,156/255,220/255)
color_transfer_function.AddRGBPoint(8 , 185/255,102/255, 83/255)
color_transfer_function.AddRGBPoint(9 , 204/255,168/255,143/255)
color_transfer_function.AddRGBPoint(10, 221/255,130/255,101/255)
color_transfer_function.AddRGBPoint(11, 197/255,165/255,145/255)
color_transfer_function.AddRGBPoint(12, 255/255,234/255, 92/255)
color_transfer_function.AddRGBPoint(13, 241/255,214/255,145/255)
color_transfer_function.AddRGBPoint(14, 157/255,108/255,162/255)
color_transfer_function.AddRGBPoint(15, 216/255,132/255,105/255)

volume_prop= vtk.vtkVolumeProperty()
volume_prop.SetColor(color_transfer_function)
volume_prop.SetScalarOpacity(opacity_transfer_function)
volume_prop.SetInterpolationTypeToLinear()


volume = vtk.vtkVolume()
volume.SetMapper(volume_mapper)
volume.SetProperty(volume_prop)

ren.AddVolume(volume)

legend = vtk.vtkLegendBoxActor();
legend.SetNumberOfEntries(15);
legendBox = vtk.vtkCubeSource();
legendBox.Update();

names = ["Blood","Brain","Duodenum","Eye retina","Eye white","Heart","Ileum","Kidney","Large intestine","Liver","Lung","Nerve","Skeleton","Spleen","Stomach"]
for i in range(1,16):
	legend.SetEntry(i-1,legendBox.GetOutput(),names[i-1],color_transfer_function.GetColor(i))

legend.GetPositionCoordinate().SetCoordinateSystemToView();
legend.GetPositionCoordinate().SetValue(.6, 0.0);

legend.GetPosition2Coordinate().SetCoordinateSystemToView();
legend.GetPosition2Coordinate().SetValue(1.1, 1);

legend.UseBackgroundOn()
legend.SetBackgroundColor([0,0,0])

ren.AddActor(legend)



aCamera = vtk.vtkCamera()
aCamera.SetViewUp(100, -1, 0)
aCamera.SetPosition(0, 0, -10)
aCamera.SetFocalPoint(0, 0, 0)
aCamera.ComputeViewPlaneNormal()

ren.SetActiveCamera(aCamera)
ren.ResetCamera()

ren.GradientBackgroundOn()
ren.SetBackground(.32,.58,.92)
ren.SetBackground2(.6,.8,.92)
renWin.SetSize(640,480)


#	Start visualization

iren.Initialize()
renWin.Render()
iren.Start()