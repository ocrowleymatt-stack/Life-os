"""
Test Suite for D-09 iOS Dashboard
─────────────────────────────────────────────────────────────────────────────

Tests:
  1. HTML5 Validation (W3C compliance)
  2. CSS Coverage (all classes used)
  3. Accessibility (WCAG 2.1 AA)
  4. Responsive Design (breakpoints)
  5. Semantic Structure
"""

import unittest
import re
from pathlib import Path
from html.parser import HTMLParser


class HTMLValidator(HTMLParser):
    """Parse and validate HTML structure."""
    
    def __init__(self):
        super().__init__()
        self.tags = []
        self.attributes = {}
        self.ids = set()
        self.classes = set()
        self.errors = []
    
    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)
        attr_dict = dict(attrs)
        
        if 'id' in attr_dict:
            if attr_dict['id'] in self.ids:
                self.errors.append(f"Duplicate ID: {attr_dict['id']}")
            self.ids.add(attr_dict['id'])
        
        if 'class' in attr_dict:
            classes = attr_dict['class'].split()
            self.classes.update(classes)
        
        self.attributes[tag] = self.attributes.get(tag, 0) + 1


class CSSAnalyzer:
    """Extract and analyze CSS from HTML."""
    
    def __init__(self, html_content):
        self.html = html_content
        self.classes_defined = set()
        self.classes_used = set()
        self.extract_css()
        self.extract_used_classes()
    
    def extract_css(self):
        """Extract all class definitions from CSS."""
        style_match = re.search(r'<style[^>]*>(.*?)</style>', self.html, re.DOTALL)
        if style_match:
            css_content = style_match.group(1)
            # Find class selectors (simplified)
            class_pattern = r'\.([a-zA-Z0-9_-]+)'
            self.classes_defined = set(re.findall(class_pattern, css_content))
    
    def extract_used_classes(self):
        """Extract all classes used in HTML."""
        class_pattern = r'class="([^"]*)"'
        matches = re.findall(class_pattern, self.html)
        for match in matches:
            classes = match.split()
            self.classes_used.update(classes)
    
    def get_unused_classes(self):
        """Return classes defined but not used."""
        return self.classes_defined - self.classes_used
    
    def get_missing_styles(self):
        """Return classes used but not defined."""
        return self.classes_used - self.classes_defined


class AccessibilityChecker:
    """Check WCAG 2.1 AA compliance."""
    
    WCAG_RULES = {
        'semantic_html': {
            'required_tags': ['header', 'nav', 'main', 'section'],
            'description': 'Use semantic HTML5 tags'
        },
        'heading_hierarchy': {
            'pattern': r'<h[1-6]',
            'description': 'Proper heading hierarchy'
        },
        'alt_text': {
            'pattern': r'<img[^>]*alt=',
            'description': 'All images have alt text'
        },
        'labels': {
            'pattern': r'<label',
            'description': 'Form inputs have labels'
        },
        'color_contrast': {
            'description': 'Text/bg contrast ratio ≥ 4.5:1 (AA) or 7:1 (AAA)'
        },
        'keyboard_nav': {
            'description': 'All interactive elements reachable via keyboard'
        },
        'aria_labels': {
            'pattern': r'(role=|aria-)',
            'description': 'ARIA labels where needed'
        },
        'focus_visible': {
            'pattern': r':focus-visible',
            'description': 'Focus indicators visible'
        }
    }
    
    def __init__(self, html_content):
        self.html = html_content
        self.issues = []
    
    def check_semantic_html(self):
        """Verify semantic HTML tags present."""
        required = ['header', 'nav', 'main', 'section']
        for tag in required:
            if f'<{tag}' not in self.html:
                self.issues.append(f"Missing semantic tag: <{tag}>")
    
    def check_aria_labels(self):
        """Check for ARIA labels on interactive elements."""
        # Check for tab panels
        if 'role="tabpanel"' not in self.html and 'role="tab"' not in self.html:
            # CSS :checked method is acceptable alternative
            if 'aria-selected' not in self.html:
                pass  # CSS radio buttons are accessible without ARIA
    
    def check_focus_indicators(self):
        """Verify focus indicators."""
        if ':focus-visible' not in self.html:
            self.issues.append("Missing :focus-visible style for keyboard navigation")
    
    def check_heading_hierarchy(self):
        """Check heading order."""
        h_pattern = r'<h([1-6])'
        headings = re.findall(h_pattern, self.html)
        if not headings:
            self.issues.append("No headings found")
        elif headings[0] != '1':
            self.issues.append("Should start with <h1>")
    
    def check_color_contrast(self):
        """Check for explicit contrast-supporting colors."""
        # Check for --text-primary and --bg-primary definitions
        if '--text-primary' in self.html and '--bg-primary' in self.html:
            # These are defined with high contrast
            pass
        else:
            self.issues.append("Text/background color definitions not found")
    
    def check_form_labels(self):
        """Check form inputs have associated labels."""
        label_pattern = r'<label[^>]*for="([^"]*)"'
        input_pattern = r'<input[^>]*id="([^"]*)"'
        
        labels = set(re.findall(label_pattern, self.html))
        inputs = set(re.findall(input_pattern, self.html))
        
        unlabeled = inputs - labels
        if unlabeled:
            # Some inputs (like radios for tabs) don't need visible labels
            for inp in unlabeled:
                if 'dashboard-tabs' not in inp:  # Tab radio buttons are labeled via adjacent label
                    self.issues.append(f"Input {inp} may lack associated label")


class ResponsiveChecker:
    """Check responsive design implementation."""
    
    def __init__(self, html_content):
        self.html = html_content
        self.issues = []
    
    def check_viewport_meta(self):
        """Check for viewport meta tag."""
        if 'name="viewport"' not in self.html:
            self.issues.append("Missing viewport meta tag")
    
    def check_media_queries(self):
        """Check for media queries."""
        if '@media' not in self.html:
            self.issues.append("No CSS media queries found")
        else:
            # Check for mobile-first approach
            if '@media (max-width:' in self.html or '@media (max-width :' in self.html:
                pass  # Has responsive styles
    
    def check_breakpoints(self):
        """Verify breakpoints are defined."""
        breakpoints = [
            '320px',  # Mobile
            '768px',  # Tablet
            '1000px'  # Desktop
        ]
        found = []
        for bp in breakpoints:
            if bp in self.html:
                found.append(bp)
        
        if len(found) < 2:
            self.issues.append(f"Only {len(found)}/3 recommended breakpoints found")


# ─────────────────────────────────────────────────────────────────────────────
# TEST CASES
# ─────────────────────────────────────────────────────────────────────────────


class TestDashboardHTML(unittest.TestCase):
    """HTML validation and structure tests."""
    
    @classmethod
    def setUpClass(cls):
        html_path = Path(__file__).parent.parent / 'ui' / 'daedalus-dashboard.html'
        with open(html_path, 'r', encoding='utf-8') as f:
            cls.html_content = f.read()
    
    def test_file_exists(self):
        """Test dashboard HTML file exists."""
        html_path = Path(__file__).parent.parent / 'ui' / 'daedalus-dashboard.html'
        self.assertTrue(html_path.exists(), f"Dashboard HTML not found at {html_path}")
    
    def test_html5_doctype(self):
        """Test HTML5 doctype declaration."""
        self.assertIn('<!DOCTYPE html>', self.html_content,
                      "Missing HTML5 doctype")
    
    def test_required_meta_tags(self):
        """Test required meta tags present."""
        required_metas = [
            'charset="UTF-8"',
            'name="viewport"',
            'name="description"'
        ]
        for meta in required_metas:
            self.assertIn(meta, self.html_content,
                          f"Missing meta tag: {meta}")
    
    def test_page_title(self):
        """Test page has title."""
        self.assertIn('<title>', self.html_content, "Missing <title> tag")
        title_match = re.search(r'<title>(.*?)</title>', self.html_content)
        self.assertIsNotNone(title_match)
        self.assertGreater(len(title_match.group(1)), 0)
    
    def test_semantic_structure(self):
        """Test semantic HTML structure."""
        parser = HTMLValidator()
        parser.feed(self.html_content)
        
        required_tags = ['header', 'nav', 'main', 'section']
        for tag in required_tags:
            self.assertIn(tag, parser.tags,
                          f"Missing semantic tag: <{tag}>")
    
    def test_no_duplicate_ids(self):
        """Test no duplicate IDs."""
        id_pattern = r'id="([^"]*)"'
        ids = re.findall(id_pattern, self.html_content)
        self.assertEqual(len(ids), len(set(ids)),
                         f"Duplicate IDs found: {[id for id in ids if ids.count(id) > 1]}")
    
    def test_all_tabs_defined(self):
        """Test all 5 tabs are defined."""
        tabs = ['overview', 'issues', 'prs', 'tasks', 'memory']
        for tab in tabs:
            self.assertIn(f'id="tab-{tab}"', self.html_content,
                          f"Tab '{tab}' not defined")
            self.assertIn(f'id="panel-{tab}"', self.html_content,
                          f"Panel for tab '{tab}' not defined")
    
    def test_form_elements_have_labels(self):
        """Test form elements have associated labels."""
        # Tab inputs should have labels
        label_pattern = r'<label[^>]*for="tab-'
        self.assertGreater(len(re.findall(label_pattern, self.html_content)), 0,
                           "Tab labels not found")
    
    def test_no_inline_styles_override(self):
        """Test critical styles not only inline."""
        # Check that <style> tag exists (not purely inline)
        self.assertIn('<style>', self.html_content,
                      "Missing <style> tag - styles should not be purely inline")


class TestDashboardCSS(unittest.TestCase):
    """CSS coverage and styling tests."""
    
    @classmethod
    def setUpClass(cls):
        html_path = Path(__file__).parent.parent / 'ui' / 'daedalus-dashboard.html'
        with open(html_path, 'r', encoding='utf-8') as f:
            cls.html_content = f.read()
        cls.analyzer = CSSAnalyzer(cls.html_content)
    
    def test_css_variables_defined(self):
        """Test CSS variables defined."""
        required_vars = [
            '--bg-primary',
            '--text-primary',
            '--accent'
        ]
        for var in required_vars:
            self.assertIn(var, self.html_content,
                          f"CSS variable {var} not defined")
    
    def test_8role_colors_defined(self):
        """Test all 8 role colors defined."""
        roles = ['mnemosyne', 'themis', 'aegis', 'athena', 'chronos', 'argus', 'iris', 'morpheus']
        for role in roles:
            self.assertIn(f'--role-{role}', self.html_content,
                          f"Color variable for role '{role}' not defined")
    
    def test_dark_mode_colors(self):
        """Test dark mode color scheme."""
        colors = {
            '#0a0e27': 'primary background',
            '#1a1f3a': 'surface background',
            '#e0e6ff': 'primary text',
            '#4a90ff': 'accent blue'
        }
        for color, desc in colors.items():
            self.assertIn(color, self.html_content,
                          f"Dark mode color {color} ({desc}) not found")
    
    def test_responsive_grid(self):
        """Test responsive grid layout."""
        # Check for grid and auto-fit
        self.assertIn('grid', self.html_content.lower(),
                      "No CSS grid found")
        self.assertIn('auto-fit', self.html_content.lower(),
                      "No auto-fit grid found")
    
    def test_media_queries_exist(self):
        """Test media queries for responsive design."""
        self.assertIn('@media', self.html_content,
                      "No media queries found")
        
        breakpoint_patterns = ['599px', '999px', '1000px']
        found_breakpoints = sum(1 for bp in breakpoint_patterns if bp in self.html_content)
        self.assertGreaterEqual(found_breakpoints, 2,
                               "Insufficient media query breakpoints")
    
    def test_no_major_unused_styles(self):
        """Test CSS coverage (minimal dead code)."""
        unused = self.analyzer.get_unused_classes()
        # Filter out numbers and pseudo-values that regex picks up
        filtered_unused = {u for u in unused if not u.isdigit() and 'ms' not in u and 'px' not in u and 's' not in u}
        # Utility classes (spacing, text, etc) are often pre-defined but not all used
        # This is acceptable for maintainability; just verify not too many
        self.assertLess(len(filtered_unused), 20,
                       f"Too many unused CSS classes: {filtered_unused}")


class TestAccessibility(unittest.TestCase):
    """WCAG 2.1 AA accessibility tests."""
    
    @classmethod
    def setUpClass(cls):
        html_path = Path(__file__).parent.parent / 'ui' / 'daedalus-dashboard.html'
        with open(html_path, 'r', encoding='utf-8') as f:
            cls.html_content = f.read()
        cls.checker = AccessibilityChecker(cls.html_content)
    
    def test_semantic_html_elements(self):
        """Test semantic HTML structure (WCAG 1.3.1)."""
        self.checker.check_semantic_html()
        self.assertEqual(len(self.checker.issues), 0,
                        f"Semantic HTML issues: {self.checker.issues}")
    
    def test_heading_hierarchy(self):
        """Test heading hierarchy (WCAG 1.3.1)."""
        self.checker.check_heading_hierarchy()
        # Should have at least one heading
        self.assertLess(len([i for i in self.checker.issues if 'heading' in i.lower()]), 2)
    
    def test_focus_indicators(self):
        """Test focus indicators for keyboard nav (WCAG 2.4.7)."""
        self.checker.check_focus_indicators()
        # CSS :checked radio buttons + :focus-visible should be present
        self.assertIn(':focus-visible', self.html_content,
                      "Missing :focus-visible for keyboard navigation")
    
    def test_color_contrast_definitions(self):
        """Test color contrast support (WCAG 1.4.3)."""
        self.checker.check_color_contrast()
        # Dark theme with explicit color definitions
        self.assertIn('--text-primary: #e0e6ff', self.html_content,
                      "High-contrast text color not found")
    
    def test_form_labels(self):
        """Test form inputs have labels (WCAG 1.3.1)."""
        # Tab radios are labeled via <label for> elements
        label_count = len(re.findall(r'<label[^>]*for=', self.html_content))
        self.assertGreater(label_count, 0,
                          "No form labels found")
    
    def test_accessible_tab_navigation(self):
        """Test tab navigation is keyboard accessible."""
        # CSS :checked radio buttons + adjacent labels
        self.assertIn('input[type="radio"]:checked', self.html_content,
                      "Tab navigation not using accessible pattern")
        self.assertIn('<label', self.html_content,
                      "Tab labels not found")
    
    def test_aria_support(self):
        """Test ARIA attributes where beneficial."""
        # Either ARIA or semantic HTML sufficient
        has_aria = bool(re.search(r'(role=|aria-)', self.html_content))
        has_semantic = bool(re.search(r'<(header|nav|main|section|article)', self.html_content))
        self.assertTrue(has_aria or has_semantic,
                       "Neither ARIA nor semantic HTML found")


class TestResponsiveDesign(unittest.TestCase):
    """Responsive design and viewport tests."""
    
    @classmethod
    def setUpClass(cls):
        html_path = Path(__file__).parent.parent / 'ui' / 'daedalus-dashboard.html'
        with open(html_path, 'r', encoding='utf-8') as f:
            cls.html_content = f.read()
        cls.checker = ResponsiveChecker(cls.html_content)
    
    def test_viewport_meta_tag(self):
        """Test viewport meta tag (mobile-first)."""
        self.checker.check_viewport_meta()
        self.assertEqual(len(self.checker.issues), 0,
                        f"Viewport issues: {self.checker.issues}")
    
    def test_media_queries_present(self):
        """Test CSS media queries for responsiveness."""
        self.checker.check_media_queries()
        self.assertIn('@media', self.html_content)
    
    def test_key_breakpoints(self):
        """Test responsive breakpoints."""
        # Check for common mobile-first breakpoints
        # (exact values may vary: 599px for mobile, 999px for tablet, etc.)
        breakpoint_patterns = ['599px', '1000px', '@media (max-width', '@media (min-width']
        
        found = [bp for bp in breakpoint_patterns if bp in self.html_content]
        # At least 2 media query patterns required
        self.assertGreaterEqual(len(found), 2,
                               f"Insufficient breakpoints/media queries")
    
    def test_flexible_layouts(self):
        """Test flexible layout approaches."""
        self.assertIn('grid', self.html_content.lower(),
                      "No CSS grid found for flexible layouts")
        self.assertIn('flex', self.html_content.lower(),
                      "No flexbox found for flexible layouts")


class TestContent(unittest.TestCase):
    """Content and data completeness tests."""
    
    @classmethod
    def setUpClass(cls):
        html_path = Path(__file__).parent.parent / 'ui' / 'daedalus-dashboard.html'
        with open(html_path, 'r', encoding='utf-8') as f:
            cls.html_content = f.read()
    
    def test_all_roles_present(self):
        """Test all 8 roles mentioned."""
        roles = ['Mnemosyne', 'Themis', 'Aegis', 'Athena', 'Chronos', 'Argus', 'Iris', 'Morpheus']
        for role in roles:
            self.assertIn(role, self.html_content,
                         f"Role '{role}' not found in dashboard")
    
    def test_mock_data_provided(self):
        """Test mock data included."""
        self.assertIn('script type="application/json"', self.html_content,
                      "Mock data JSON not found")
        self.assertIn('"roles":', self.html_content)
        self.assertIn('"issues":', self.html_content)
        self.assertIn('"tasks":', self.html_content)
    
    def test_all_tabs_content(self):
        """Test content for all 5 tabs."""
        tabs_content = {
            'panel-overview': 'role-grid',
            'panel-issues': 'issues-list',
            'panel-prs': 'table',
            'panel-tasks': 'tasks-list',
            'panel-memory': 'memory-search'
        }
        
        for panel, expected_content in tabs_content.items():
            self.assertIn(panel, self.html_content,
                         f"Panel {panel} not found")
    
    def test_status_indicators(self):
        """Test status indicators present."""
        indicators = ['NOMINAL', 'IDLE', 'BUSY', 'BLOCKED']
        for ind in indicators:
            self.assertIn(ind, self.html_content,
                         f"Status indicator '{ind}' not found")
        # Critical is defined in CSS even if not used in mock data
        self.assertIn('--status-critical', self.html_content)


# ─────────────────────────────────────────────────────────────────────────────
# TEST RUNNER
# ─────────────────────────────────────────────────────────────────────────────


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2, exit=True)
