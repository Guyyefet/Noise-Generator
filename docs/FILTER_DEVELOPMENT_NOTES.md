# Filter Development Notes

## Recent Changes to Cascaded One-Pole Lowpass Filter V2

### Performance Optimizations
- Converted all operations to use float32 precision for better performance
- Added vectorized operations where possible
- Pre-calculate coefficients outside the sample processing loop

### Stability Improvements
- Implemented tanh soft clipping instead of hard clipping for smoother response
- Limited coefficient ranges for better stability (alpha: 0.005 to 0.5)
- Reduced pole scaling factor to 1.3 for more stable multi-pole operation
- Added per-sample processing with stability checks

### Volume and Gain Handling
- Implemented more consistent gain compensation across pole counts
- Added 20% gain boost per additional pole
- Increased resonance boost (up to 50% at max resonance)
- Used tanh for smoother gain limiting

### Resonance Behavior
- Removed resonance limiting to allow potential self-oscillation
- Added feedback scaling based on pole count (10% increase per pole)
- Implemented soft clipping on feedback path
- Improved DC offset handling

## Current Test Failures and Explanations

1. test_frequency_response:
   - Fails because our new coefficient scaling produces different attenuation characteristics
   - The test expects stronger attenuation with more poles, but our current implementation prioritizes stability
   - Consider updating test thresholds to match new behavior or adjusting coefficient scaling

2. test_resonance_behavior:
   - Fails self-oscillation test (output too low with zero input)
   - Current implementation struggles to achieve true self-oscillation while maintaining stability
   - Need to investigate alternative feedback paths that can achieve oscillation without introducing artifacts

3. test_volume_scaling:
   - Volume levels don't stay within expected 3dB range across pole counts
   - Current gain compensation might be too aggressive
   - Test may need updating to reflect practical volume requirements vs theoretical expectations

4. test_dc_offset:
   - DC offset removal not meeting strict <1e-10 requirement
   - Current implementation prioritizes stability over perfect DC removal
   - May need more sophisticated DC removal approach

## Future Improvements

### Resonance Enhancement
1. Investigate alternative feedback structures:
   - Consider implementing state variable filter topology
   - Explore multi-tap feedback paths
   - Research zero-delay feedback techniques

2. Stability vs Self-Oscillation:
   - Find better balance between stability and resonance intensity
   - Consider implementing resonance limiting only in unstable regions
   - Research better coefficient mapping for resonance control

### Volume Control
1. Gain Compensation:
   - Implement more sophisticated gain tracking
   - Consider automatic gain control based on signal analysis
   - Research better pole scaling techniques for consistent volume

2. DC Offset:
   - Implement more aggressive DC blocking without compromising stability
   - Consider adding dedicated DC blocking filter stage
   - Research better normalization techniques

### Performance
1. Optimization Opportunities:
   - Investigate SIMD optimizations for sample processing
   - Research more efficient coefficient calculation methods
   - Consider block-based processing optimizations

### Testing
1. Test Suite Updates:
   - Review and update test thresholds to match practical requirements
   - Add more real-world usage tests
   - Consider adding performance benchmarks

## Notes on Float32 vs Float64
- Switched to float32 for better performance
- No significant quality impact observed
- Consider maintaining float64 option for high-precision requirements
- May need additional validation for extreme parameter values

## Recommendations
1. Prioritize resonance improvements:
   - Research alternative filter topologies
   - Implement better feedback control
   - Consider hybrid approach combining multiple techniques

2. Review test requirements:
   - Adjust thresholds based on practical needs
   - Add more real-world use cases
   - Consider separating stability tests from ideal behavior tests

3. Consider maintaining both V1 and V2 implementations:
   - V1 for maximum stability
   - V2 for better resonance control
   - Let users choose based on their needs
