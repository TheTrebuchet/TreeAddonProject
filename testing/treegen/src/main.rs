use noise::{NoiseFn, Perlin, Seedable};

fn main() {
	use std::time::Instant;
	let now = Instant::now();

	{
		let perlin = Perlin::new(1);
		let n = 1000000;
		let mut v = Vec::new();
		for i in 1..n {
			let coord = i as f64/(n as f64)*100.0;
			let val = perlin.get([coord, coord, coord]);
			v.push(val);
		}
		let s: f64 = v.iter().sum();
		println!("{}",s);
	}
	let elapsed = now.elapsed();
	println!("Elapsed: {:.2?}", elapsed);
}
