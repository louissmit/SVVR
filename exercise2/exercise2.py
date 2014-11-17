#!/usr/bin/env python
import vtk


#Starting value for the contourfilter
initial_v = 2750
#Min value slider
min_v = 500
#Max value slider
max_v = 5000



#Creation of renderer, window and iteractor
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)



#====Reading in the data using a Volume16Reader
v16 = vtk.vtkVolume16Reader()
v16.SetDataDimensions(256,256)
v16.SetFilePrefix("MysteryData/slice")
v16.SetImageRange(1, 94)
v16.SetDataSpacing(1, 1, 2)
#==============================================

#====Creation of the contour filter ============
# This is the variable contour filter
contour_skeleton = vtk.vtkContourFilter()
contour_skeleton.SetInputConnection(v16.GetOutputPort())
contour_skeleton.SetValue(0, initial_v)
contour_skeleton.ComputeNormalsOn()

# Create normals for smoother rendereing
normals_skeleton = vtk.vtkPolyDataNormals()
normals_skeleton.SetInputConnection(contour_skeleton.GetOutputPort())
normals_skeleton.SetFeatureAngle(60.0)

# Map the data to a certain range
mapper_skeleton = vtk.vtkPolyDataMapper()
mapper_skeleton.SetScalarRange(500,5000)
mapper_skeleton.SetInputConnection(normals_skeleton.GetOutputPort())

# Create the actor used for coloring
skeleton = vtk.vtkActor()
skeleton.SetMapper(mapper_skeleton)

ren.AddActor(skeleton)
#==============================================

#====Creation of the opaque skin ==============
contour_skin = vtk.vtkContourFilter()
contour_skin.SetInputConnection(v16.GetOutputPort())
contour_skin.SetValue(0, 500) #500 is the value for skin
contour_skin.ComputeNormalsOn()
contour_skin.ComputeScalarsOff() #remove blue color

mapper_skin = vtk.vtkPolyDataMapper()
mapper_skin.SetInputConnection(contour_skin.GetOutputPort())

skin = vtk.vtkActor()
skin.SetMapper(mapper_skin)

# Set skin color and opacity. Is transparent to show to data inside in context
skin.GetProperty().SetColor(.7,.7,.7)
skin.GetProperty().SetOpacity(.2)

ren.AddActor(skin)
#==============================================

#====Creation of a bounding box================
outlineData = vtk.vtkOutlineFilter()
outlineData.SetInputConnection(v16.GetOutputPort())
mapOutline = vtk.vtkPolyDataMapper()
mapOutline.SetInputConnection(outlineData.GetOutputPort())
outline = vtk.vtkActor()
outline.SetMapper(mapOutline)
outline.GetProperty().SetColor(0.5, 0.5, 0.5)

ren.AddActor(outline)
#==============================================

#====Camera====================================
aCamera = vtk.vtkCamera()
aCamera.SetViewUp(0, 0, -1)
aCamera.SetPosition(-1, 1, 0)
aCamera.SetFocalPoint(0, 0, 0)
aCamera.ComputeViewPlaneNormal()


ren.SetActiveCamera(aCamera)
ren.ResetCamera()

aCamera.Dolly(1.5)
#==============================================


#====Change window settings====================
# Set a background color for the renderer
ren.SetBackground(.1, .1, .1)
# Set windows size in pixels
renWin.SetSize(640, 480)
ren.ResetCameraClippingRange()
#==============================================



# Initialize the interactor and render for the first time
iren.Initialize()
renWin.Render()

#=======Slider Creation========================
def vtkSliderCallback2(obj, event):
    sliderRepres = obj.GetRepresentation()
    pos = sliderRepres.GetValue()
    contour_skeleton.SetValue(0, pos)

SliderRepres = vtk.vtkSliderRepresentation2D()

SliderRepres.SetMinimumValue(min_v)
SliderRepres.SetMaximumValue(max_v)


SliderRepres.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
SliderRepres.GetPoint1Coordinate().SetValue(0.2, 0.1)
SliderRepres.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
SliderRepres.GetPoint2Coordinate().SetValue(0.8, 0.1)

SliderRepres.SetSliderLength(0.02)
SliderRepres.SetSliderWidth(0.03)
SliderRepres.SetEndCapLength(0.01)
SliderRepres.SetEndCapWidth(0.01)
SliderRepres.SetTubeWidth(0.005)
SliderRepres.SetLabelFormat("%3.0lf")
SliderRepres.SetTitleHeight(0.02)
SliderRepres.SetLabelHeight(0.02)

SliderWidget = vtk.vtkSliderWidget()
SliderWidget.SetInteractor(iren)
SliderWidget.SetRepresentation(SliderRepres)
SliderWidget.KeyPressActivationOff()
SliderWidget.SetAnimationModeToAnimate()
SliderWidget.SetEnabled(True)
SliderWidget.AddObserver("EndInteractionEvent", vtkSliderCallback2)

SliderRepres.SetValue(initial_v)
#==============================================

#Start the interaction
iren.Start()
