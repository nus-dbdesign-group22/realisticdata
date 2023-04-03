import random

from generator_types.base import BaseTypeGenerator


class DepartmentName(BaseTypeGenerator):
    department_name = ["Aerospace Engineering",
                       "Biosciences and Bioengineering",
                       "Chemical Engineering",
                       "Chemistry",
                       "Civil Engineering",
                       "Computer Science & Engineering",
                       "Earth Sciences",
                       "Electrical Engineering",
                       "Energy Science and Engineering",
                       "Humanities & Social Science",
                       "Mathematics",
                       "Mechanical Engineering",
                       "Metallurgical Engineering & Materials Science",
                       "Physics",
                       "Industrial Design Centre",
                       "Application Software Centre (ASC)",
                       "Centre for Research in Nanotechnology and Science (CRNTS)",
                       "Centre for Aerospace Systems Design and Engineering (CASDE)",
                       "Computer Centre (CC)",
                       "Centre for Distance Engineering Education Programme (CDEEP)",
                       "Centre for Environmental Science and Engineering (CESE)",
                       "Centre for Policy Studies (CPS)",
                       "Centre of Studies in Resources Engineering (CSRE)",
                       "Centre for Technology Alternatives for Rural Areas (CTARA)",
                       "Centre for Formal Design and Verification of Software (CFDVS)",
                       "Centre for Urban Science and Engineering (C-USE)",
                       "Centre for Entrepreneurship (DSCE)",
                       "ABC-EDS Research Academy",
                       "National Centre for Aerospace Innovation and Research (NCAIR)",
                       "National Center of Excellence in Technology for Internal Security (NCETIS)",
                       "National Centre for Mathematics (NCM)",
                       "Center for Learning and Teaching (PPCCLT)",
                       "Sophisticated Analytical Instrument Facility (SAIF)",
                       "Technology and Design (TCTD)",
                       "Centre for Bioengineering (WRCB)",
                       "School of Management",
                       "Climate Studies",
                       "Educational Technology",
                       "Industrial Engineering and Operations Research (IEOR)",
                       "Systems and Control Engineering"]

    def get_next_value(self, related_values=None) -> any:
        sample = random.choice(self.department_name)
        return sample
