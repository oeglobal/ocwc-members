# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2019-01-17 04:48
from __future__ import unicode_literals

import arrow
from django.db import migrations

data = (
    ('0145', u'Massachusetts Institute of Technology', '19/10/2005'),
    ('0369', u'Utah State University', '28/01/2007'),
    ('0143', u'Tecnológico de Monterrey', '17/01/2008'),
    ('0228', u'Commonwealth of Learning (COL)', '25/03/2008'),
    ('0215', u'UNIVERSIA', '01/04/2008'),
    ('0053', u'Universidad Politécnica de Valencia', '09/04/2008'),
    ('0089', u'Universidad Politécnica Madrid', '11/04/2008'),
    ('0202', u'Mountain Heights Academy', '04/06/2008'),
    ('0132', u'University of California, Irvine', '13/08/2008'),
    ('0117', u'Tufts University', '07/10/2008'),
    ('0127', u'Universidad de Zaragoza', '07/10/2008'),
    ('0123', u'University of Michigan', '07/10/2008'),
    ('0014', u'Universidad Icesi', '27/10/2008'),
    ('0036', u'Universidad de Cantabria', '10/01/2009'),
    ('0227', u'Creative Commons', '12/01/2009'),
    ('0068', u'Universidad de La Laguna', '01/04/2009'),
    ('0277', u'University of the People', '16/04/2009'),
    ('0190', u'Ankara University', '01/06/2009'),
    ('0102', u'Bahá\'í Institute for Higher Education', '01/06/2009'),
    ('0050', u'EduNet Vietnam', '01/06/2009'),
    ('0235', u'European Association of Distance Teaching Universities (EADTU)', '01/06/2009'),
    ('0060', u'Fu Jen Catholic University', '01/06/2009'),
    ('0151', u'Hokkaido University', '01/06/2009'),
    ('0209', u'iBerry', '01/06/2009'),
    ('0099', u'IUI - Farabi Institute of Higher Education', '01/06/2009'),
    ('0370', u'Japan OCW Consortium', '01/06/2009'),
    ('0038', u'Kabul Polytechnic University', '01/06/2009'),
    ('0083', u'Kagawa Nutrition University', '01/06/2009'),
    ('0100', u'Kyoto University', '01/06/2009'),
    ('0150', u'Kyushu University', '01/06/2009'),
    ('0074', u'Middle East Technical University', '01/06/2009'),
    ('0101', u'Nagoya University', '01/06/2009'),
    ('0046', u'National Cheng Kung University', '01/06/2009'),
    ('0075', u'National Chengchi University', '01/06/2009'),
    ('0146', u'National Chiao Tung University', '01/06/2009'),
    ('0065', u'National Sun Yat-Sen University', '01/06/2009'),
    ('0059', u'National Taiwan Normal University', '01/06/2009'),
    ('0107', u'National Tsing Hua University', '01/06/2009'),
    ('0447', u'Netease Information Technology (Beijing) Co., Ltd', '01/06/2009'),
    ('0226', u'OER Africa', '01/06/2009'),
    ('0222', u'OOPS', '01/06/2009'),
    ('0112', u'Open University Netherlands', '01/06/2009'),
    ('0129', u'Osaka University', '01/06/2009'),
    ('0206', u'Paris Tech', '01/06/2009'),
    ('0152', u'People\'s Open Access Education Initiative', '01/06/2009'),
    ('0031', u'Taipei Medical University', '01/06/2009'),
    ('0213', u'Taiwan Open Course and Education Consortium', '01/06/2009'),
    ('0139', u'The Open University', '01/06/2009'),
    ('0001', u'The Open University of Israel', '01/06/2009'),
    ('0013', u'The University of Nottingham', '01/06/2009'),
    ('0098', u'Tokyo Institute of Technology', '01/06/2009'),
    ('0147', u'TU Delft', '01/06/2009'),
    ('0214', u'Turkish OpenCourseWare Consortium', '01/06/2009'),
    ('0072', u'Université de Lyon', '01/06/2009'),
    ('0113', u'University of Southern Queensland', '01/06/2009'),
    ('0119', u'University of Tokyo', '01/06/2009'),
    ('0079', u'University of Tsukuba', '01/06/2009'),
    ('0141', u'Waseda University', '01/06/2009'),
    ('0270', u'Teachers Without Borders', '13/07/2009'),
    ('0120', u'Johns Hopkins Bloomberg School of Public Health', '12/10/2009'),
    ('0134', u'Universidad Carlos III de Madrid', '19/10/2009'),
    ('0009', u'Fundação Getulio Vargas - FGV Online', '26/10/2009'),
    ('0088', u'Universidad Nacional de Educacion a Distancia', '03/11/2009'),
    ('0071', u'Universidad Estatal a Distancia', '09/11/2009'),
    ('0062', u'Centro de Ensino Superior Strong', '13/11/2009'),
    ('0124', u'Athabasca University', '15/12/2009'),
    ('0237', u'MERLOT - Multimedia Educational Resource for Learning and Online Teaching', '18/12/2009'),
    ('0371', u'UNISUL - Universidade do Sul de Santa Catarina', '01/01/2010'),
    ('0381', u'Washington State Board for Community and Technical Colleges', '01/01/2010'),
    ('0372', u'AGH University of Science and Technology', '15/01/2010'),
    ('0404', u'University of Cape Town', '01/02/2010'),
    ('0409', u'International Christian University', '15/03/2010'),
    ('0412', u'Kwansei Gakuin University', '15/03/2010'),
    ('0413', u'The Open University of Japan', '15/03/2010'),
    ('0408', u'Universitas Indonesia', '15/03/2010'),
    ('0427', u'University of Malaya', '01/07/2010'),
    ('0376', u'Soochow University', '15/07/2010'),
    ('0428', u'Virtual University of Pakistan', '15/07/2010'),
    ('0432', u'African Virtual University', '01/09/2010'),
    ('0431', u'National Open University of Nigeria', '01/09/2010'),
    ('0434', u'VIA University College, Denmark', '16/11/2010'),
    ('0448', u'CCCOER - Community College Consortium for Open Educational Resources', '28/01/2011'),
    ('0437', u'Sophia University', '28/01/2011'),
    ('0444', u'Universiti Teknologi Malaysia', '15/03/2011'),
    ('0457', u'The Saylor Foundation', '29/03/2011'),
    ('0477', u'Peer 2 Peer University', '23/05/2011'),
    ('0474', u'Shanghai Jiaotong U', '23/05/2011'),
    ('0489', u'Hungkuang University', '05/07/2011'),
    ('0491', u'Kun Shan University', '05/07/2011'),
    ('0479', u'National Central Univeristy', '05/07/2011'),
    ('0481', u'National Chung Hsing University', '05/07/2011'),
    ('0484', u'National Dong Hwa University', '05/07/2011'),
    ('0486', u'National Taiwan Ocean University', '05/07/2011'),
    ('0480', u'National Taiwan University', '05/07/2011'),
    ('0482', u'Providence University', '05/07/2011'),
    ('0497', u'Universidad Técnica Particular de Loja', '15/07/2011'),
    ('0500', u'National Open University', '04/08/2011'),
    ('0501', u'Kirkwood Community College', '24/08/2011'),
    ('0502', u'San Diego Community College District', '24/08/2011'),
    ('0510', u'Sterling College', '04/10/2011'),
    ('0515', u'National Pingtung University of Science and Technology (NPUST)', '13/10/2011'),
    ('0522', u'University of West Florida', '13/10/2011'),
    ('0528', u'SURFnet', '04/01/2012'),
    ('0532', u'College of the Canyons', '23/01/2012'),
    ('0537', u'Universidad Nacional Autónoma de México UNAM', '15/02/2012'),
    ('0538', u'Pasadena City College', '23/02/2012'),
    ('0539', u'Houston Community College District', '06/03/2012'),
    ('0543', u'Chung Hua University', '23/03/2012'),
    ('0549', u'Eastern Mediterranean University', '22/05/2012'),
    ('0550', u'Universitat Politècnica de Catalunya. BarcelonaTech UPC)', '22/05/2012'),
    ('0552', u'Oregon Community College Distance Learning Association', '29/06/2012'),
    ('0558', u'University of Leuven (KU Leuven)', '07/09/2012'),
    ('0561', u'Maricopa Community Colleges', '22/10/2012'),
    ('0569', u'Northern Virginia Community College (NOVA)', '12/11/2012'),
    ('0568', u'Universitas Terbuka (Indonesian Open University)', '13/12/2012'),
    ('0581', u'BC Campus', '29/01/2013'),
    ('0577', u'Open Education France', '15/02/2013'),
    ('0586', u'California Community Colleges Chancellor’s Office', '15/03/2013'),
    ('0589', u'Jozef Stefan Institute', '20/03/2013'),
    ('0584', u'Greek Academic Network OCW/OER Consortium', '30/04/2013'),
    ('0595', u'National Ilan University', '30/04/2013'),
    ('0591', u'University of Maryland University College', '30/04/2013'),
    ('0598', u'American Public University System', '15/06/2013'),
    ('0594', u'Instituto Israelita de Ensino e Pesquisa Albert Einstein', '15/06/2013'),
    ('0600', u'Broward College', '12/08/2013'),
    ('0603', u'Cuyahoga Community College', '30/09/2013'),
    ('0605', u'Organisation Internationale de la Francophonie', '07/10/2013'),
    ('0608', u'Michigan Community College Virtual Learning Collaborative', '30/10/2013'),
    ('0610', u'IMT-Atlantique - Telecom Bretagne', '14/11/2013'),
    ('0619', u'Chattanooga State Comunity College', '03/02/2014'),
    ('0621', u'ETH Zurich', '14/02/2014'),
    ('0622', u'Università Telematica Internazionale UNINETTUNO', '14/02/2014'),
    ('0625', u'Delaware County Community College', '05/03/2014'),
    ('0623', u'Open College at Kaplan University (OC@KU)', '05/03/2014'),
    ('0630', u'Lektorium LLC', '14/03/2014'),
    ('0629', u'University of Nantes', '14/03/2014'),
    ('0637', u'Tidewater Community College', '15/04/2014'),
    ('0636', u'Virginia Community College System', '15/04/2014'),
    ('0635', u'GO-GN', '18/04/2014'),
    ('0633', u'Universiti Sains Malaysia (USM)', '18/04/2014'),
    ('0632', u'Universiti Teknikal Malaysia Melaka', '18/04/2014'),
    ('0648', u'Mohave Community College', '29/05/2014'),
    ('0639', u'Universiti Malaysia Sarawak', '30/06/2014'),
    ('0640', u'Universiti Teknologi MARA', '30/06/2014'),
    ('0652', u'Universiti Putra Malaysia (UPM)', '16/07/2014'),
    ('0651', u'Citrus Community College District', '30/07/2014'),
    ('0650', u'Connecticut State Colleges & Universities', '30/07/2014'),
    ('0649', u'MarylandOnline', '30/07/2014'),
    ('0655', u'Universiti Pendidikan Sultan Idris (Sultan Idris Education University)', '16/09/2014'),
    ('0656', u'University Kebangsaan Malaysia (UKM)', '30/09/2014'),
    ('0660', u'College of DuPage', '22/10/2014'),
    ('0658', u'Moscow Institute of Physics and Technology (MIPT)', '22/10/2014'),
    ('0661', u'Boston\'s Children Hospital', '18/11/2014'),
    ('0664', u'Lord Fairfax Community College', '09/02/2015'),
    ('0663', u'Tamkang University', '30/03/2015'),
    ('0669', u'North Central Texas College', '17/04/2015'),
    ('0668', u'Northern Essex Community College', '17/04/2015'),
    ('0672', u'Bay De Noc Community College', '30/06/2015'),
    ('0670', u'Hanze University of Applied Sciences', '13/07/2015'),
    ('0673', u'E-Open Institute, Mongolian University Of Science and Technology', '17/07/2015'),
    ('0671', u'Swinburne University of Technology', '10/08/2015'),
    ('0676', u'Universiti Malaysia Sabah', '31/08/2015'),
    ('0674', u'Dallas County Community College District', '10/09/2015'),
    ('0675', u'Universidad Nacional de Cordoba', '10/09/2015'),
    ('0662', u'Fontys University of Applied Sciences, School of ICT', '15/09/2015'),
    ('0677', u'Universidade Federal de Santa Catarina (UFSC)', '15/09/2015'),
    ('0679', u'College of Lake County', '30/10/2015'),
    ('0678', u'University of Massachusetts Dartmouth', '30/10/2015'),
    ('0033', u'Arizona State University', '30/11/2015'),
    ('0680', u'Salt Lake Community College', '30/11/2015'),
    ('0683', u'Alamo Colleges', '15/01/2016'),
    ('0682', u'Training and Development Network', '15/01/2016'),
    ('0685', u'Universite Republicaine d\'Haiti', '15/02/2016'),
    ('0686', u'Oregon State University', '23/02/2016'),
    ('0687', u'North Shore Community College', '04/05/2016'),
    ('0688', u'California Community Colleges Online Education Initiative (OEI)', '07/06/2016'),
    ('0689', u'Austin Community College District', '15/06/2016'),
    ('0691', u'Harford Community College', '15/09/2016'),
    ('0693', u'Darakht-e Danesh Library', '28/09/2016'),
    ('0694', u'eVidhya.com', '28/09/2016'),
    ('0692', u'The University of the South Pacific', '28/09/2016'),
    ('0695', u'Contact North', '30/09/2016'),
    ('0696', u'University of New Hampshire', '30/09/2016'),
    ('0699', u'Granite State University', '08/11/2016'),
    ('0700', u'Keene State University', '08/11/2016'),
    ('0701', u'Lansing Community College', '08/11/2016'),
    ('0698', u'Plymouth State University', '08/11/2016'),
    ('0702', u'Bucks County Community College', '15/12/2016'),
    ('0706', u'Charles Sturt University', '01/02/2017'),
    ('0704', u'Ivy Tech Community College', '06/02/2017'),
    ('0705', u'Santa Fe College', '06/02/2017'),
    ('0707', u'Lakeland Community College', '20/02/2017'),
    ('0709', u'Pierce College', '20/02/2017'),
    ('0708', u'Ventura County Community College District', '20/02/2017'),
    ('0710', u'San Jose City College', '20/03/2017'),
    ('0711', u'MiraCosta College', '17/04/2017'),
    ('0713', u'Mitchell Community College', '05/05/2017'),
    ('0715', u'Columbus State Community College', '15/05/2017'),
    ('0714', u'SUNY OER Services', '15/05/2017'),
    ('0717', u'Northwestern Michigan College', '30/06/2017'),
    ('0716', u'Technical College System of Georgia', '30/06/2017'),
    ('0718', u'Allan Hancock College', '30/07/2017'),
    ('0719', u'Nicolet College', '30/07/2017'),
    ('0723', u'Taylor\'s University Lakeside Campus, Malaysia', '04/08/2017'),
    ('0725', u'Front Range Community College', '15/08/2017'),
    ('0724', u'Mercer County Community College', '16/08/2017'),
    ('0697', u'Norwegian Digital Learning Arena', '14/10/2017'),
    ('0743', u'AUNEGE - French Thematic Digital University for Economics and Management', '15/11/2017'),
    ('0740', u'eCampus Ontario', '20/11/2017'),
    ('0738', u'Minesota State University, Mankato', '20/11/2017'),
    ('0742', u'North Rhine-Westphalian Library Service Centre (hbz) / OER World Map', '20/11/2017'),
    ('0741', u'Taft College', '20/11/2017'),
    ('0739', u'Union County College', '20/11/2017'),
    ('0744', u'KlasCement.net', '11/12/2017'),
    ('0747', u'INACAP', '13/12/2017'),
    ('0746', u'Southern New Hampshire University', '13/12/2017'),
    ('0748', u'University of Hawaii Community Colleges (Leeward Community College', '13/12/2017'),
    ('0745', u'West Hills College Lemoore', '13/12/2017'),
    ('0749', u'Saxion University of Applied Sciences', '30/01/2018'),
    ('0753', u'Butte-Glenn Community College District', '09/02/2018'),
    ('0553', u'Lakeshore Technical College', '10/02/2018'),
    ('0752', u'Raritan Valley Community College', '11/02/2018'),
    ('0751', u'Central Maine Community College', '12/02/2018'),
    ('0750', u'Mount Wachusett Community College', '13/02/2018'),
    ('0755', u'Massasoit Community College', '07/05/2018'),
    ('0756', u'City University of New York (CUNY)', '20/06/2018'),
    ('0758', u'Hinds Community College', '25/06/2018'),
    ('0759', u'Politecnico di Milano', '28/06/2018'),
    ('0757', u'Université catholique de Louvain (UCLouvain)', '28/06/2018'),
    ('0762', u'Central Carolina Community College', '22/08/2018'),
    ('0761', u'College of Southern Nevada', '22/08/2018'),
    ('0763', u'Fox Valley Technical College Library', '22/08/2018'),
    ('0760', u'Covenant University', '28/09/2018'),
    ('0768', u'Central Lakes College', '22/10/2018'),
    ('0767', u'Roxbury Community College', '22/10/2018'),
    ('0766', u'Trident Technical College', '22/10/2018'),
    ('0765', u'Windward Community College', '22/10/2018'),
    ('0770', u'Achieving the Dream', '20/11/2018'),
    ('0769', u'Grayson College', '20/11/2018'),
    ('0764', u'Moodle', '12/12/2018'),
)


def forwards(apps, schema_editor):
    Organization = apps.get_model("crm", "Organization")

    for line in data:
        org_id, name, date = line

        org = Organization.objects.get(pk=int(org_id))
        org.created = arrow.get(date, 'DD/MM/YYYY').datetime
        org.save()


class Migration(migrations.Migration):
    dependencies = [
        ('crm', '0014_auto_20190117_0402'),
    ]

    operations = [
        migrations.RunPython(forwards, hints={'target_db': 'default'}),
    ]
