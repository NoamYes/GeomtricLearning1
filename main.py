from read_off import read_off 
from write_off import write_off 

(v, f) = read_off('off_files/example_off_files/sphere_s0.off')
write_off('output.off', v, f)
