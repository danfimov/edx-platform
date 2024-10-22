"""Tests for CRUD Operations"""


from xmodule import templates
from xmodule.capa_block import ProblemBlock
from xmodule.course_block import CourseBlock
from xmodule.html_block import HtmlBlock
from xmodule.modulestore import ModuleStoreEnum
from xmodule.modulestore.exceptions import DuplicateCourseError
from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase
from xmodule.modulestore.tests.factories import CourseFactory, BlockFactory
from xmodule.seq_block import SequenceBlock


class TemplateTests(ModuleStoreTestCase):
    """
    Test finding and using the templates (boilerplates) for xblocks.
    """
    def test_get_templates(self):
        found = templates.all_templates()
        assert found.get('course') is not None
        assert found.get('about') is not None
        assert found.get('html') is not None
        assert found.get('problem') is not None
        assert len(found.get('course')) == 0
        assert len(found.get('about')) == 1
        self.assertGreaterEqual(len(found.get('html')), 2)
        self.assertGreaterEqual(len(found.get('problem')), 10)
        dropdown = None
        for template in found['problem']:
            self.assertIn('metadata', template)
            self.assertIn('display_name', template['metadata'])
            if template['metadata']['display_name'] == 'Dropdown':
                dropdown = template
                break
        assert dropdown is not None
        self.assertIn('markdown', dropdown['metadata'])
        self.assertIn('data', dropdown)
        self.assertRegex(dropdown['metadata']['markdown'], r'.*dropdown problems.*')
        self.assertRegex(dropdown['data'], r'<problem>\s*<optionresponse>\s*<p>.*dropdown problems.*')

    def test_get_some_templates(self):
        assert len(SequenceBlock.templates()) == 0
        self.assertGreater(len(HtmlBlock.templates()), 0)
        assert SequenceBlock.get_template('doesntexist.yaml') is None
        assert HtmlBlock.get_template('doesntexist.yaml') is None
        assert HtmlBlock.get_template('announcement.yaml') is not None

    def test_factories(self):
        test_course = CourseFactory.create(
            org='testx',
            course='course',
            run='2014',
            display_name='fun test course',
            user_id=ModuleStoreEnum.UserID.test,
        )
        assert isinstance(test_course, CourseBlock)
        assert test_course.display_name == 'fun test course'
        course_from_store = self.store.get_course(test_course.id)
        assert course_from_store.id.org == 'testx'
        assert course_from_store.id.course == 'course'
        assert course_from_store.id.run == '2014'

        test_chapter = BlockFactory.create(
            parent_location=test_course.location,
            category='chapter',
            display_name='chapter 1'
        )
        assert isinstance(test_chapter, SequenceBlock)
        # refetch parent which should now point to child
        test_course = self.store.get_course(test_course.id.version_agnostic())
        self.assertIn(test_chapter.location, test_course.children)

        with self.assertRaises(DuplicateCourseError):
            CourseFactory.create(
                org='testx',
                course='course',
                run='2014',
                display_name='fun test course',
                user_id=ModuleStoreEnum.UserID.test,
            )

    def test_temporary_xblocks(self):
        """
        Test create_xblock to create non persisted xblocks
        """
        test_course = CourseFactory.create(
            course='course', run='2014', org='testx',
            display_name='fun test course', user_id=ModuleStoreEnum.UserID.test,
        )

        test_chapter = self.store.create_xblock(
            test_course.runtime, test_course.id, 'chapter', fields={'display_name': 'chapter n'},
            parent_xblock=test_course
        )
        assert isinstance(test_chapter, SequenceBlock)
        assert test_chapter.display_name == 'chapter n'
        self.assertIn(test_chapter, test_course.get_children())

        # test w/ a definition (e.g., a problem)
        test_def_content = '<problem>boo</problem>'
        test_problem = self.store.create_xblock(
            test_course.runtime, test_course.id, 'problem', fields={'data': test_def_content},
            parent_xblock=test_chapter
        )
        assert isinstance(test_problem, ProblemBlock)
        assert test_problem.data == test_def_content
        self.assertIn(test_problem, test_chapter.get_children())
        test_problem.display_name = 'test problem'
        assert test_problem.display_name == 'test problem'

    def test_delete_course(self):
        test_course = CourseFactory.create(
            org='edu.harvard',
            course='history',
            run='doomed',
            display_name='doomed test course',
            user_id=ModuleStoreEnum.UserID.test,
        )
        BlockFactory.create(
            parent_location=test_course.location,
            category='chapter',
            display_name='chapter 1'
        )

        id_locator = test_course.id.for_branch(ModuleStoreEnum.BranchName.draft)
        # verify it can be retrieved by id
        assert isinstance(self.store.get_course(id_locator), CourseBlock)
        # TODO reenable when split_draft supports getting specific versions
        # guid_locator = test_course.location.course_agnostic()
        # Verify it can be retrieved by guid
        # assert isinstance(self.store.get_item(guid_locator), CourseBlock)
        self.store.delete_course(id_locator, ModuleStoreEnum.UserID.test)
        # Test can no longer retrieve by id.
        assert self.store.get_course(id_locator) is None
        # But can retrieve by guid -- same TODO as above
        # assert isinstance(self.store.get_item(guid_locator), CourseBlock)
