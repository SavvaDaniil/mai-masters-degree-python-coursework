
from typing import List

from maionline.models import CourseLesson, CourseLessonSlide

from maionline.repository.CourseLessonSlideRepository import CourseLessonSlideRepository
from maionline.factory.CourseLessonSlideFactory import CourseLessonSlideFactory
from maionline.viewmodel.CourseLessonSlideViewModel import CourseLessonSlideLiteViewModel

class CourseLessonSlideFacade():

    def __init__(self):
        self.courseLessonSlideRepository: CourseLessonSlideRepository = CourseLessonSlideRepository()
        self.courseLessonSlideFactory: CourseLessonSlideFactory = CourseLessonSlideFactory()

    def list_slides_by_course_lesson(self, courseLesson: CourseLesson) -> List[str]:
        slides: List[str] = []
        courseLessonSlides: List[CourseLessonSlide] = self.courseLessonSlideRepository.list_by_course_lesson(courseLesson=courseLesson)
        for courseLessonSlide in courseLessonSlides:
            slides.append(courseLessonSlide.getImageSrc())
        return slides

    def list_info_by_course_lesson(self, courseLesson: CourseLesson) -> List[CourseLessonSlideLiteViewModel]:
        courseLessonSlideLiteViewModels: List[CourseLessonSlideLiteViewModel] = []
        courseLessonSlides: List[CourseLessonSlide] = self.courseLessonSlideRepository.list_by_course_lesson(courseLesson=courseLesson)
        for courseLessonSlide in courseLessonSlides:
            courseLessonSlideLiteViewModels.append(
                self.courseLessonSlideFactory.create_lite(courseLessonSlide=courseLessonSlide)
            )
        return courseLessonSlideLiteViewModels

    