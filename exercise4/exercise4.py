from __future__ import division
import sys

if len(sys.argv) != 2:
  print "Usage: " + sys.argv[0] + " <Folder to frog(Tissue).***.raw>"
  sys.exit()

import vtk

def get_reader(file_prefix):
	reader = vtk.vtkImageReader()
	reader.SetFilePrefix(file_prefix)
	reader.SetFilePattern('%s%03d.raw')
	reader.SetDataScalarTypeToUnsignedChar()
	reader.SetFileDimensionality(2)
	reader.SetDataSpacing(1,1,1.5)
	reader.SetDataExtent(0,499,0,469,1,136)
	reader.Update()
	return reader

skin_color = (0,1,0) 

tissue_config = {}  
tissue_config['Blood'] 			= (1 ,(232 /255, 0 /255, 0 /255),.7)
tissue_config['Brain'] 			= (2 ,(180 /255, 56 /255, 180 /255),.7)
tissue_config['Duodenum'] 		= (3 ,(255 /255, 255 /255, 68 /255),.7)	
tissue_config['Eye retina'] 	= (4 ,(100 /255, 149 /255, 237 /255),.7)
tissue_config['Eye white'] 		= (5 ,(232 /255, 232 /255, 232 /255),.7)		
tissue_config['Heart'] 			= (6 ,(249 /255, 69 /255, 0 /255),.7)	
tissue_config['Ileum'] 			= (7 ,(255 /255, 182 /255, 193 /255),.7)
tissue_config['Kidney'] 		= (8 ,(139 /255, 69 /255, 19 /255),.7)	
tissue_config['Large Intestine']= (9 ,(255 /255, 20 /255, 147 /255),.7) 	
tissue_config['Liver'] 			= (10,(249 /255, 201 /255, 144 /255),.1)
tissue_config['Lung'] 			= (11,(0 /255, 181 /255, 117 /255),.7)	
tissue_config['Nerve'] 			= (12,(255 /255, 215 /255, 0 /255),.7)	
tissue_config['Skeleton'] 		= (13,(255 /255, 255 /255, 255 /255), .1)	
tissue_config['Spleen']			= (14,(188 /255, 139 /255, 172 /255),.7)
tissue_config['Stomach'] 		= (15,(106 /255, 90 /255, 205 /255),.7)

106-90-205

frog_dir = sys.argv[1]

ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

frog_reader = get_reader(frog_dir+'frog.')

frog_contour = vtk.vtkContourFilter()
frog_contour.SetInputConnection(frog_reader.GetOutputPort())
frog_contour.SetValue(0,10)
frog_contour.ComputeScalarsOff()

frog_mapper = vtk.vtkPolyDataMapper()
frog_mapper.SetInputConnection(frog_contour.GetOutputPort())

frog_actor = vtk.vtkActor()
frog_actor.SetMapper(frog_mapper)
frog_actor.GetProperty().SetOpacity(0.1)
frog_actor.GetProperty().SetColor(*skin_color)

ren.AddActor(frog_actor)

tissue_reader = get_reader(frog_dir + 'frogTissue.')

composite_function = vtk.vtkVolumeRayCastCompositeFunction()
composite_function.SetCompositeMethodToClassifyFirst()
volume_mapper = vtk.vtkVolumeRayCastMapper()
volume_mapper.SetVolumeRayCastFunction(composite_function)
volume_mapper.SetInputConnection(tissue_reader.GetOutputPort())

opacity_transfer_function = vtk.vtkPiecewiseFunction()
opacity_transfer_function.AddPoint(0, 0)
opacity_transfer_function.AddPoint(16, 0)

color_transfer_function = vtk.vtkColorTransferFunction()
color_transfer_function.AddRGBPoint(0,0,0,0)
color_transfer_function.AddRGBPoint(16,0,0,0)

legend = vtk.vtkLegendBoxActor()
legend.SetNumberOfEntries(15)

legendBox = vtk.vtkCubeSource()
legendBox.Update()

legend.GetPositionCoordinate().SetCoordinateSystemToView()
legend.GetPositionCoordinate().SetValue(.55, 0.0)
legend.GetPosition2Coordinate().SetCoordinateSystemToView()
legend.GetPosition2Coordinate().SetValue(1, .99)
legend.SetPadding(10)
legend.UseBackgroundOn()
legend.SetBackgroundColor([0,0,0])
legend.SetBackgroundOpacity(0.5)

for tissue_name, (point, tissue_color, tissue_opacity) in tissue_config.items():

	opacity_transfer_function.AddPoint(point,tissue_opacity)
	color_transfer_function.AddRGBPoint(point,*tissue_color)
	
	legend.SetEntry(point-1,legendBox.GetOutput(),tissue_name,tissue_color)



volume_prop = vtk.vtkVolumeProperty()
volume_prop.SetColor(color_transfer_function)
volume_prop.SetScalarOpacity(opacity_transfer_function)
volume_prop.SetInterpolationTypeToLinear()

volume = vtk.vtkVolume()
volume.SetMapper(volume_mapper)
volume.SetProperty(volume_prop)

ren.AddVolume(volume)
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

iren.Initialize()
renWin.Render()
iren.Start()