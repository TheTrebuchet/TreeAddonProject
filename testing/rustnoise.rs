use noise::{Fbm, Perlin};
use noise::utils::{NoiseMapBuilder, PlaneMapBuilder};

fn main() {
  let fbm = Fbm::<Perlin>::new(0);

  PlaneMapBuilder::<_, 2>::new(&fbm)
          .set_size(1000, 1000)
          .set_x_bounds(-5.0, 5.0)
          .set_y_bounds(-5.0, 5.0)
          .build()
          .write_to_file("fbm.png");
}


