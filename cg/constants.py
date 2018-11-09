# -*- coding: utf-8 -*-

PRIORITY_MAP = {'research': 0, 'standard': 1, 'priority': 2, 'express': 3}
REV_PRIORITY_MAP = {value: key for key, value in PRIORITY_MAP.items()}
PRIORITY_OPTIONS = list(PRIORITY_MAP.keys())
FAMILY_ACTIONS = ('analyze', 'running', 'hold')
PREP_CATEGORIES = ('wgs', 'wes', 'tgs', 'wts', 'mic', 'rml')
SEX_OPTIONS = ('male', 'female', 'unknown')
STATUS_OPTIONS = ('affected', 'unaffected', 'unknown')
CONTAINER_OPTIONS = ('Tube', '96 well plate')
CAPTUREKIT_OPTIONS = ('Agilent Sureselect CRE',
                      'Agilent Sureselect V5',
                      'SureSelect Focused Exome',
                      'Twist_Target_hg19.bed',
                      'other')
CAPTUREKIT_CANCER_OPTIONS = ('Twist exome v1.3',
                             'Twist panel CG001',
                             'Nimblegen MSK-IMPACT')
FLOWCELL_STATUS = ('ondisk', 'removed', 'requested', 'processing')
