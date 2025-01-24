
from maionline.models import CourseLessonSlide
from maionline.viewmodel.CourseLessonSlideViewModel import CourseLessonSlideLiteViewModel

class CourseLessonSlideFactory():

    def create_lite(self, courseLessonSlide: CourseLessonSlide) -> CourseLessonSlideLiteViewModel:
        return CourseLessonSlideLiteViewModel(
            id=courseLessonSlide.id,
            url=courseLessonSlide.getImageSrc(),
            order_in_list=courseLessonSlide.order_in_list
        )