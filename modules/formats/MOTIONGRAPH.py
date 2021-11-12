def collect_motiongraph(self, ss_entry):
    # Sized string initpos = position of first fragment
    print(ss_entry.pointers[0].address, len(ss_entry.pointers[0].data))
    if self.ovl.basename.lower() == "driver.ovl":
        print("Debug mode for driver motiongraph!")
        print()
        for frag in self.fragments:
            if 10036 <= frag.pointers[1].address < 10700:
                # ss_entry.fragments.append(frag)
                frag.pointers[1].strip_zstring_padding()
                frag.name = frag.pointers[1].data[:-1]  # .decode()

        f = self.frags_from_pointer(ss_entry.pointers[0], 4)
        u0, u1, counts, name_ptr = f
        d2 = struct.unpack("<4I", counts.pointers[0].data)
        print("counts", d2)
        _, _, unk_count, name_count_1 = d2
        ss_entry.names_1 = self.frags_from_pointer(name_ptr.pointers[1], name_count_1)
        for n in ss_entry.names_1:
            print(n.pointers[1].data)
        d3 = struct.unpack("<3Q", counts.pointers[1].data)
        _, two, one = d3
        print(d3)
        k = self.frags_from_pointer(counts.pointers[1], 9)
        for i in k:
            z = struct.unpack("<3Q", i.pointers[0].data)
            print(z)

# count, _ = struct.unpack("<2I", ss_entry.pointers[0].data)
# # print(count)
# ss_entry.vars = self.frags_from_pointer(ss_entry.fragments[0].pointers[1], count)
# # pointers[1].data is the name
# for var in ss_entry.vars:
# 	var.pointers[1].strip_zstring_padding()
# # The last fragment has padding that may be junk data to pad the size of the name block to multiples of 64
# ss_entry.fragments.extend(ss_entry.vars)