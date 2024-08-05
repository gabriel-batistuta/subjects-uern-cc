import lib

if __name__ == "__main__":
    url = 'https://www.uern.br/cursos/servico.asp?fac=FANAT&cur_cd=1018100&grd_cd=20012&cur_nome=Ci%EAncia+da+Computa%E7%E3o&grd_medint=8&item=grade'
    page = lib.get_page(url)
    course_dict = lib.get_course_info(page)
    hours_dict = lib.get_hours_info(page)
    subjects_list = lib.get_subjects(page)
    lib.make_json({
        'course_info': course_dict,
        'hours_info': hours_dict,
        'subjects': subjects_list
    })