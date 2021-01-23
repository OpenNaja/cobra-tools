import os
from modules.formats.shared import djb
from generated.array import Array
import io


def file_remover(ovl, filenames):
    for filename in filenames:
        new_dd = Array()
        new_bb = Array()
        new_f = Array()
        basename, fileext = os.path.splitext(filename)
        # remove file entry
        for i, file_entry in enumerate(ovl.files):
            if basename == file_entry.name and file_entry.ext == fileext:

                del_hash = file_entry.file_hash

                ovl.files.pop(i)
                ovl.num_files -= 1
                ovl.num_files_2 -= 1
                ovl.num_files_3 -= 1

                # update mime entries TODO: remove mime if no more files left in it
                kk = file_entry.extension
                for k, mime in enumerate(ovl.mimes):
                    if k == kk:
                        # found mime matching removed file
                        ovl.mimes[k].file_count -= 1
                    elif k > kk:
                        ovl.mimes[k].file_index_offset -= 1
                # remove dependencies for removed file
                old_dep_len = len(ovl.dependencies)
                for dep in ovl.dependencies:
                    if dep.file_index != i:
                        if dep.file_index > i:
                            dep.file_index -= 1
                        new_dd.append(dep)
                ovl.dependencies = new_dd
                ovl.num_dependencies -= old_dep_len - len(ovl.dependencies)

                # remove sizedstring entry for file and remove its fragments if mapped
                for ss, string in enumerate(ovl.archives[0].content.sized_str_entries):
                    if string.lower_name == file_entry.name + "." + fileext:
                        ovl.archives[0].content.sized_str_entries.pop(ss)
                        ovl.archives[0].num_files -= 1
                        ovl.archives[0].uncompressed_size -= 16

                        str_adr = string.pointers[0].address
                        th = 0

                        string.pointers[0].update_data(b"", update_copies=True)
                        for frag in string.fragments:
                            frag.pointers[0].update_data(b"", update_copies=True)
                            frag.pointers[1].update_data(b"", update_copies=True)

                        fgg = []
                        for frg in string.fragments:
                            fgg.append(frg.o_ind)

                        rem_ff = len(fgg)

                        for fff in ovl.archives[0].content.fragments:
                            if fff.o_ind not in fgg:
                                new_f.append(fff)

                        ovl.archives[0].content.fragments = new_f
                        ovl.archives[0].num_fragments -= rem_ff

                # TODO UPDATE THE HEADER ENTRIES WITH THE FIRST FILE HASH AND NEW COUNTS

                # remove data entry for file
                for de, data in enumerate(ovl.archives[0].content.data_entries):
                    if data.basename == file_entry.name and data.ext == fileext:

                        ovl.archives[0].num_datas -= 1
                        ovl.num_datas -= 1
                        ovl.archives[0].uncompressed_size -= 32

                        zero_buff_array = []
                        for i, buffer in enumerate(data.buffer_datas):
                            zero_buff_array.append(b"")
                        data.update_data(zero_buff_array)
                        thing = []
                        for buff in data.buffers:
                            thing.append(buff.o_ind)
                        thing.sort()
                        rem_buf = len(thing)

                        for bbf in ovl.archives[0].content.buffer_entries:
                            if bbf.o_ind not in thing:
                                new_bb.append(bbf)

                        ovl.archives[0].content.buffer_entries = new_bb
                        ovl.archives[0].num_buffers -= rem_buf
                        ovl.num_buffers -= rem_buf

                        ovl.archives[0].uncompressed_size -= 8 * rem_buf
                        ovl.archives[0].content.data_entries.pop(de)
            print(i)
            new_dd = Array()
            new_bb = Array()
            new_f = Array()
