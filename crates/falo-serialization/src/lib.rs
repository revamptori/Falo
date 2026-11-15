use serde::{Deserialize, Serialize};
use anyhow::Result;

pub fn to_ron<T: Serialize>(v: &T) -> Result<String> { Ok(ron::to_string(v)?) }
pub fn from_ron<T: for<'de> Deserialize<'de>>(s: &str) -> Result<T> { Ok(ron::from_str(s)?) }
pub fn to_bin<T: Serialize>(v: &T) -> Result<Vec<u8>> { Ok(rmp_serde::to_vec_named(v)?) }
pub fn from_bin<T: for<'de> Deserialize<'de>>(b: &[u8]) -> Result<T> { Ok(rmp_serde::from_slice(b)?) }
