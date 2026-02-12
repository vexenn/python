import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from flask import Flask, render_template, render_template_string, jsonify
import base64
from io import BytesIO
import json

app = Flask(__name__)

# ECG Waveform Generation Functions
def generate_normal_canine_ecg(duration=2, heart_rate=120):
    """Generate normal canine ECG"""
    samples = int(duration * 1000)
    t = np.linspace(0, duration, samples)
    ecg = np.zeros(samples)
    
    beat_interval = 60 / heart_rate
    num_beats = int(duration / beat_interval)
    
    for beat in range(num_beats):
        offset = beat * beat_interval
        
        # P wave (atrial depolarization)
        p_mask = (t >= offset + 0.05) & (t < offset + 0.15)
        ecg[p_mask] += 0.15 * np.sin(np.pi * (t[p_mask] - offset - 0.05) / 0.1)
        
        # QRS complex (ventricular depolarization)
        # Q wave
        q_mask = (t >= offset + 0.2) & (t < offset + 0.23)
        ecg[q_mask] -= 0.1 * np.sin(np.pi * (t[q_mask] - offset - 0.2) / 0.03)
        
        # R wave
        r_mask = (t >= offset + 0.23) & (t < offset + 0.27)
        ecg[r_mask] += 1.5 * np.sin(np.pi * (t[r_mask] - offset - 0.23) / 0.04)
        
        # S wave
        s_mask = (t >= offset + 0.27) & (t < offset + 0.3)
        ecg[s_mask] -= 0.2 * np.sin(np.pi * (t[s_mask] - offset - 0.27) / 0.03)
        
        # T wave (ventricular repolarization)
        t_mask = (t >= offset + 0.35) & (t < offset + 0.5)
        ecg[t_mask] += 0.25 * np.sin(np.pi * (t[t_mask] - offset - 0.35) / 0.15)
    
    return t, ecg

def generate_normal_feline_ecg(duration=2, heart_rate=180):
    """Generate normal feline ECG"""
    samples = int(duration * 1000)
    t = np.linspace(0, duration, samples)
    ecg = np.zeros(samples)
    
    beat_interval = 60 / heart_rate
    num_beats = int(duration / beat_interval)
    
    for beat in range(num_beats):
        offset = beat * beat_interval
        
        # P wave (smaller in cats)
        p_mask = (t >= offset + 0.02) & (t < offset + 0.08)
        ecg[p_mask] += 0.1 * np.sin(np.pi * (t[p_mask] - offset - 0.02) / 0.06)
        
        # QRS complex (narrow in cats)
        q_mask = (t >= offset + 0.12) & (t < offset + 0.14)
        ecg[q_mask] -= 0.08 * np.sin(np.pi * (t[q_mask] - offset - 0.12) / 0.02)
        
        r_mask = (t >= offset + 0.14) & (t < offset + 0.17)
        ecg[r_mask] += 1.2 * np.sin(np.pi * (t[r_mask] - offset - 0.14) / 0.03)
        
        s_mask = (t >= offset + 0.17) & (t < offset + 0.19)
        ecg[s_mask] -= 0.15 * np.sin(np.pi * (t[s_mask] - offset - 0.17) / 0.02)
        
        # T wave (variable in cats)
        t_mask = (t >= offset + 0.22) & (t < offset + 0.32)
        ecg[t_mask] += 0.15 * np.sin(np.pi * (t[t_mask] - offset - 0.22) / 0.1)
    
    return t, ecg

def generate_normal_equine_ecg(duration=2, heart_rate=40):
    """Generate normal equine ECG pattern"""
    samples = int(duration * 1000)
    t = np.linspace(0, duration, samples)
    ecg = np.zeros(samples)
    
    beat_interval = 60.0 / heart_rate
    num_beats = int(duration / beat_interval)
    
    for beat in range(num_beats):
        offset = beat * beat_interval
        
        # Large P wave (horses have large atria)
        p_mask = (t >= offset + 0.05) & (t < offset + 0.2)
        ecg[p_mask] += 0.3 * np.sin(np.pi * (t[p_mask] - offset - 0.05) / 0.15)
        
        # Long PR interval
        # Q wave
        q_mask = (t >= offset + 0.4) & (t < offset + 0.45)
        ecg[q_mask] -= 0.15 * np.sin(np.pi * (t[q_mask] - offset - 0.4) / 0.05)
        
        # R wave (can be variable in horses)
        r_mask = (t >= offset + 0.45) & (t < offset + 0.52)
        ecg[r_mask] += 1.2 * np.sin(np.pi * (t[r_mask] - offset - 0.45) / 0.07)
        
        # S wave
        s_mask = (t >= offset + 0.52) & (t < offset + 0.58)
        ecg[s_mask] -= 0.25 * np.sin(np.pi * (t[s_mask] - offset - 0.52) / 0.06)
        
        # T wave (can be biphasic in horses)
        t_mask = (t >= offset + 0.7) & (t < offset + 0.85)
        ecg[t_mask] += 0.2 * np.sin(np.pi * (t[t_mask] - offset - 0.7) / 0.15)
        
        # Second phase of T wave (biphasic)
        t2_mask = (t >= offset + 0.85) & (t < offset + 1.0)
        ecg[t2_mask] -= 0.1 * np.sin(np.pi * (t[t2_mask] - offset - 0.85) / 0.15)
    
    return t, ecg

def generate_atrial_fibrillation(duration=2):
    """Generate atrial fibrillation pattern"""
    samples = int(duration * 1000)
    t = np.linspace(0, duration, samples)
    ecg = np.zeros(samples)
    
    # Add fibrillatory waves (irregular baseline)
    ecg += 0.05 * np.random.randn(samples)
    for freq in [8, 12, 15]:
        phase = np.random.rand() * 2 * np.pi
        ecg += 0.03 * np.sin(2 * np.pi * freq * t + phase)
    
    # Irregularly irregular R-R intervals
    intervals = np.random.uniform(0.4, 0.9, 20)
    offset = 0
    
    for interval in intervals:
        if offset + 0.3 > duration:
            break
            
        # QRS complex (narrow, no P waves)
        q_mask = (t >= offset) & (t < offset + 0.02)
        ecg[q_mask] -= 0.08 * np.sin(np.pi * (t[q_mask] - offset) / 0.02)
        
        r_mask = (t >= offset + 0.02) & (t < offset + 0.06)
        ecg[r_mask] += 1.3 * np.sin(np.pi * (t[r_mask] - offset - 0.02) / 0.04)
        
        s_mask = (t >= offset + 0.06) & (t < offset + 0.08)
        ecg[s_mask] -= 0.12 * np.sin(np.pi * (t[s_mask] - offset - 0.06) / 0.02)
        
        # T wave
        t_mask = (t >= offset + 0.15) & (t < offset + 0.28)
        ecg[t_mask] += 0.2 * np.sin(np.pi * (t[t_mask] - offset - 0.15) / 0.13)
        
        offset += interval
    
    return t, ecg

def generate_atrial_flutter(duration=2):
    """Generate atrial flutter pattern"""
    samples = int(duration * 1000)
    t = np.linspace(0, duration, samples)
    ecg = np.zeros(samples)
    
    # Flutter waves (sawtooth pattern)
    flutter_rate = 300  # atrial rate
    flutter_interval = 60.0 / flutter_rate
    
    num_flutter = int(duration / flutter_interval)
    for i in range(num_flutter):
        offset = i * flutter_interval
        f_mask = (t >= offset) & (t < offset + flutter_interval)
        ecg[f_mask] += 0.1 * np.sin(2 * np.pi * (t[f_mask] - offset) / flutter_interval)
    
    # QRS complexes with variable block (2:1, 3:1, 4:1)
    ventricular_interval = 0.5  # 2:1 block example
    num_beats = int(duration / ventricular_interval)
    
    for beat in range(num_beats):
        offset = beat * ventricular_interval
        
        # QRS complex
        q_mask = (t >= offset + 0.1) & (t < offset + 0.12)
        ecg[q_mask] -= 0.1 * np.sin(np.pi * (t[q_mask] - offset - 0.1) / 0.02)
        
        r_mask = (t >= offset + 0.12) & (t < offset + 0.16)
        ecg[r_mask] += 1.4 * np.sin(np.pi * (t[r_mask] - offset - 0.12) / 0.04)
        
        s_mask = (t >= offset + 0.16) & (t < offset + 0.18)
        ecg[s_mask] -= 0.15 * np.sin(np.pi * (t[s_mask] - offset - 0.16) / 0.02)
        
        # T wave
        t_mask = (t >= offset + 0.25) & (t < offset + 0.38)
        ecg[t_mask] += 0.22 * np.sin(np.pi * (t[t_mask] - offset - 0.25) / 0.13)
    
    return t, ecg

def generate_ventricular_tachycardia(duration=2):
    """Generate ventricular tachycardia"""
    samples = int(duration * 1000)
    t = np.linspace(0, duration, samples)
    ecg = np.zeros(samples)
    
    beat_interval = 0.35  # Fast rate
    num_beats = int(duration / beat_interval)
    
    for beat in range(num_beats):
        offset = beat * beat_interval
        
        # Wide, bizarre QRS complexes
        # No clear P waves
        
        q_mask = (t >= offset) & (t < offset + 0.05)
        ecg[q_mask] -= 0.3 * np.sin(np.pi * (t[q_mask] - offset) / 0.05)
        
        r_mask = (t >= offset + 0.05) & (t < offset + 0.15)
        ecg[r_mask] += 2.0 * np.sin(np.pi * (t[r_mask] - offset - 0.05) / 0.1)
        
        # Add some irregularity to morphology
        ecg[r_mask] += 0.3 * np.sin(3 * np.pi * (t[r_mask] - offset - 0.05) / 0.1)
        
        s_mask = (t >= offset + 0.15) & (t < offset + 0.22)
        ecg[s_mask] -= 0.5 * np.sin(np.pi * (t[s_mask] - offset - 0.15) / 0.07)
        
        # Wide T wave
        t_mask = (t >= offset + 0.25) & (t < offset + 0.33)
        ecg[t_mask] += 0.4 * np.sin(np.pi * (t[t_mask] - offset - 0.25) / 0.08)
    
    return t, ecg

def generate_av_block_first_degree(duration=2):
    """Generate first-degree AV block"""
    samples = int(duration * 1000)
    t = np.linspace(0, duration, samples)
    ecg = np.zeros(samples)
    
    beat_interval = 0.8
    num_beats = int(duration / beat_interval)
    
    for beat in range(num_beats):
        offset = beat * beat_interval
        
        # P wave
        p_mask = (t >= offset + 0.05) & (t < offset + 0.15)
        ecg[p_mask] += 0.15 * np.sin(np.pi * (t[p_mask] - offset - 0.05) / 0.1)
        
        # Prolonged PR interval (> 0.13s in dogs)
        # QRS starts later than normal
        q_mask = (t >= offset + 0.28) & (t < offset + 0.31)
        ecg[q_mask] -= 0.1 * np.sin(np.pi * (t[q_mask] - offset - 0.28) / 0.03)
        
        r_mask = (t >= offset + 0.31) & (t < offset + 0.35)
        ecg[r_mask] += 1.5 * np.sin(np.pi * (t[r_mask] - offset - 0.31) / 0.04)
        
        s_mask = (t >= offset + 0.35) & (t < offset + 0.38)
        ecg[s_mask] -= 0.2 * np.sin(np.pi * (t[s_mask] - offset - 0.35) / 0.03)
        
        # T wave
        t_mask = (t >= offset + 0.45) & (t < offset + 0.6)
        ecg[t_mask] += 0.25 * np.sin(np.pi * (t[t_mask] - offset - 0.45) / 0.15)
    
    return t, ecg

def generate_av_block_second_degree(duration=2):
    """Generate second-degree AV block (Mobitz II)"""
    samples = int(duration * 1000)
    t = np.linspace(0, duration, samples)
    ecg = np.zeros(samples)
    
    beat_interval = 0.8
    num_beats = int(duration / beat_interval)
    
    for beat in range(num_beats):
        offset = beat * beat_interval
        
        # P wave (always present)
        p_mask = (t >= offset + 0.05) & (t < offset + 0.15)
        ecg[p_mask] += 0.15 * np.sin(np.pi * (t[p_mask] - offset - 0.05) / 0.1)
        
        # Every 3rd or 4th P wave has no QRS (dropped beat)
        if beat % 3 != 2:  # Skip every 3rd beat
            # QRS complex
            q_mask = (t >= offset + 0.2) & (t < offset + 0.23)
            ecg[q_mask] -= 0.1 * np.sin(np.pi * (t[q_mask] - offset - 0.2) / 0.03)
            
            r_mask = (t >= offset + 0.23) & (t < offset + 0.27)
            ecg[r_mask] += 1.5 * np.sin(np.pi * (t[r_mask] - offset - 0.23) / 0.04)
            
            s_mask = (t >= offset + 0.27) & (t < offset + 0.3)
            ecg[s_mask] -= 0.2 * np.sin(np.pi * (t[s_mask] - offset - 0.27) / 0.03)
            
            # T wave
            t_mask = (t >= offset + 0.35) & (t < offset + 0.5)
            ecg[t_mask] += 0.25 * np.sin(np.pi * (t[t_mask] - offset - 0.35) / 0.15)
    
    return t, ecg

def generate_av_block_third_degree(duration=2):
    """Generate third-degree (complete) AV block"""
    samples = int(duration * 1000)
    t = np.linspace(0, duration, samples)
    ecg = np.zeros(samples)
    
    # Atrial rate (P waves)
    atrial_interval = 0.6
    num_p_waves = int(duration / atrial_interval)
    
    for beat in range(num_p_waves):
        offset = beat * atrial_interval
        p_mask = (t >= offset) & (t < offset + 0.1)
        ecg[p_mask] += 0.15 * np.sin(np.pi * (t[p_mask] - offset) / 0.1)
    
    # Ventricular rate (QRS complexes) - slower and independent
    ventricular_interval = 1.0
    num_qrs = int(duration / ventricular_interval)
    
    for beat in range(num_qrs):
        offset = beat * ventricular_interval + 0.15  # Offset to show dissociation
        
        # Wide QRS (ventricular escape rhythm)
        q_mask = (t >= offset) & (t < offset + 0.05)
        ecg[q_mask] -= 0.15 * np.sin(np.pi * (t[q_mask] - offset) / 0.05)
        
        r_mask = (t >= offset + 0.05) & (t < offset + 0.15)
        ecg[r_mask] += 1.8 * np.sin(np.pi * (t[r_mask] - offset - 0.05) / 0.1)
        
        s_mask = (t >= offset + 0.15) & (t < offset + 0.22)
        ecg[s_mask] -= 0.3 * np.sin(np.pi * (t[s_mask] - offset - 0.15) / 0.07)
        
        # T wave
        t_mask = (t >= offset + 0.3) & (t < offset + 0.5)
        ecg[t_mask] += 0.3 * np.sin(np.pi * (t[t_mask] - offset - 0.3) / 0.2)
    
    return t, ecg

def generate_left_bundle_branch_block(duration=2):
    """Generate left bundle branch block"""
    samples = int(duration * 1000)
    t = np.linspace(0, duration, samples)
    ecg = np.zeros(samples)
    
    beat_interval = 0.8
    num_beats = int(duration / beat_interval)
    
    for beat in range(num_beats):
        offset = beat * beat_interval
        
        # P wave
        p_mask = (t >= offset + 0.05) & (t < offset + 0.15)
        ecg[p_mask] += 0.15 * np.sin(np.pi * (t[p_mask] - offset - 0.05) / 0.1)
        
        # Wide QRS complex (> 0.08s) with notched R wave
        q_mask = (t >= offset + 0.2) & (t < offset + 0.23)
        ecg[q_mask] -= 0.08 * np.sin(np.pi * (t[q_mask] - offset - 0.2) / 0.03)
        
        # Notched R wave (characteristic of LBBB)
        r1_mask = (t >= offset + 0.23) & (t < offset + 0.28)
        ecg[r1_mask] += 1.2 * np.sin(np.pi * (t[r1_mask] - offset - 0.23) / 0.05)
        
        # Notch
        notch_mask = (t >= offset + 0.28) & (t < offset + 0.3)
        ecg[notch_mask] += 0.8 * np.sin(np.pi * (t[notch_mask] - offset - 0.28) / 0.02)
        
        # Second R peak
        r2_mask = (t >= offset + 0.3) & (t < offset + 0.35)
        ecg[r2_mask] += 1.4 * np.sin(np.pi * (t[r2_mask] - offset - 0.3) / 0.05)
        
        s_mask = (t >= offset + 0.35) & (t < offset + 0.38)
        ecg[s_mask] -= 0.15 * np.sin(np.pi * (t[s_mask] - offset - 0.35) / 0.03)
        
        # T wave
        t_mask = (t >= offset + 0.45) & (t < offset + 0.6)
        ecg[t_mask] += 0.2 * np.sin(np.pi * (t[t_mask] - offset - 0.45) / 0.15)
    
    return t, ecg

def generate_right_bundle_branch_block(duration=2):
    """Generate right bundle branch block"""
    samples = int(duration * 1000)
    t = np.linspace(0, duration, samples)
    ecg = np.zeros(samples)
    
    beat_interval = 0.8
    num_beats = int(duration / beat_interval)
    
    for beat in range(num_beats):
        offset = beat * beat_interval
        
        # P wave
        p_mask = (t >= offset + 0.05) & (t < offset + 0.15)
        ecg[p_mask] += 0.15 * np.sin(np.pi * (t[p_mask] - offset - 0.05) / 0.1)
        
        # Wide QRS with RSR' pattern (M-shaped)
        # R wave
        r1_mask = (t >= offset + 0.2) & (t < offset + 0.24)
        ecg[r1_mask] += 1.0 * np.sin(np.pi * (t[r1_mask] - offset - 0.2) / 0.04)
        
        # S wave
        s_mask = (t >= offset + 0.24) & (t < offset + 0.28)
        ecg[s_mask] -= 0.5 * np.sin(np.pi * (t[s_mask] - offset - 0.24) / 0.04)
        
        # R' wave (second R wave - characteristic of RBBB)
        r2_mask = (t >= offset + 0.28) & (t < offset + 0.34)
        ecg[r2_mask] += 1.3 * np.sin(np.pi * (t[r2_mask] - offset - 0.28) / 0.06)
        
        # Final S wave
        s2_mask = (t >= offset + 0.34) & (t < offset + 0.38)
        ecg[s2_mask] -= 0.2 * np.sin(np.pi * (t[s2_mask] - offset - 0.34) / 0.04)
        
        # T wave
        t_mask = (t >= offset + 0.45) & (t < offset + 0.6)
        ecg[t_mask] += 0.22 * np.sin(np.pi * (t[t_mask] - offset - 0.45) / 0.15)
    
    return t, ecg

def generate_asystole(duration=2):
    """Generate asystole (flat line)"""
    samples = int(duration * 1000)
    t = np.linspace(0, duration, samples)
    # Just baseline noise
    ecg = 0.02 * np.random.randn(samples)
    
    return t, ecg

def generate_ventricular_fibrillation(duration=2):
    """Generate ventricular fibrillation"""
    samples = int(duration * 1000)
    t = np.linspace(0, duration, samples)
    
    # Chaotic, irregular waveform
    ecg = np.zeros(samples)
    
    # Multiple overlapping frequencies
    for freq in np.random.uniform(5, 20, 15):
        amplitude = np.random.uniform(0.1, 0.5)
        phase = np.random.rand() * 2 * np.pi
        ecg += amplitude * np.sin(2 * np.pi * freq * t + phase)
    
    # Add random noise
    ecg += 0.2 * np.random.randn(samples)
    
    return t, ecg

def generate_premature_ventricular_contraction(duration=2):
    """Generate normal rhythm with PVCs"""
    samples = int(duration * 1000)
    t = np.linspace(0, duration, samples)
    ecg = np.zeros(samples)
    
    # Normal beats
    normal_beats = [0, 0.8, 2.4]  # Skip one position for PVC
    
    for offset in normal_beats:
        if offset >= duration:
            continue
            
        # P wave
        p_mask = (t >= offset + 0.05) & (t < offset + 0.15)
        ecg[p_mask] += 0.15 * np.sin(np.pi * (t[p_mask] - offset - 0.05) / 0.1)
        
        # Normal QRS
        q_mask = (t >= offset + 0.2) & (t < offset + 0.23)
        ecg[q_mask] -= 0.1 * np.sin(np.pi * (t[q_mask] - offset - 0.2) / 0.03)
        
        r_mask = (t >= offset + 0.23) & (t < offset + 0.27)
        ecg[r_mask] += 1.5 * np.sin(np.pi * (t[r_mask] - offset - 0.23) / 0.04)
        
        s_mask = (t >= offset + 0.27) & (t < offset + 0.3)
        ecg[s_mask] -= 0.2 * np.sin(np.pi * (t[s_mask] - offset - 0.27) / 0.03)
        
        # T wave
        t_mask = (t >= offset + 0.35) & (t < offset + 0.5)
        ecg[t_mask] += 0.25 * np.sin(np.pi * (t[t_mask] - offset - 0.35) / 0.15)
    
    # PVC at 1.6 seconds (premature, wide, bizarre)
    pvc_offset = 1.6
    if pvc_offset < duration:
        # No P wave before PVC
        
        # Wide, bizarre QRS
        q_mask = (t >= pvc_offset) & (t < pvc_offset + 0.05)
        ecg[q_mask] -= 0.3 * np.sin(np.pi * (t[q_mask] - pvc_offset) / 0.05)
        
        r_mask = (t >= pvc_offset + 0.05) & (t < pvc_offset + 0.15)
        ecg[r_mask] += 2.2 * np.sin(np.pi * (t[r_mask] - pvc_offset - 0.05) / 0.1)
        
        s_mask = (t >= pvc_offset + 0.15) & (t < pvc_offset + 0.22)
        ecg[s_mask] -= 0.6 * np.sin(np.pi * (t[s_mask] - pvc_offset - 0.15) / 0.07)
        
        # Inverted T wave
        t_mask = (t >= pvc_offset + 0.25) & (t < pvc_offset + 0.4)
        ecg[t_mask] -= 0.4 * np.sin(np.pi * (t[t_mask] - pvc_offset - 0.25) / 0.15)
    
    return t, ecg

def generate_ventricular_tachycardia(duration=2):
    """Generate ventricular tachycardia pattern"""
    samples = int(duration * 1000)
    t = np.linspace(0, duration, samples)
    ecg = np.zeros(samples)
    
    beat_interval = 0.3  # Very fast rate
    num_beats = int(duration / beat_interval)
    
    for beat in range(num_beats):
        offset = beat * beat_interval
        
        # Wide, bizarre QRS complexes
        qrs_mask = (t >= offset) & (t < offset + 0.15)
        ecg[qrs_mask] += 1.8 * np.sin(np.pi * (t[qrs_mask] - offset) / 0.15)
        ecg[qrs_mask] += 0.5 * np.sin(3 * np.pi * (t[qrs_mask] - offset) / 0.15)
    
    return t, ecg

def generate_atrial_fibrillation(duration=2):
    """Generate atrial fibrillation pattern"""
    samples = int(duration * 1000)
    t = np.linspace(0, duration, samples)
    ecg = np.zeros(samples)
    
    # Irregular baseline (fibrillatory waves)
    ecg += 0.05 * np.random.randn(samples)
    
    # Irregular R-R intervals
    beat_times = [0]
    while beat_times[-1] < duration:
        interval = np.random.uniform(0.3, 0.7)
        beat_times.append(beat_times[-1] + interval)
    
    for offset in beat_times[:-1]:
        # QRS complex only (no P waves)
        r_idx = int(offset * 1000)
        if r_idx < samples - 50:
            r_mask = (t >= offset) & (t < offset + 0.08)
            ecg[r_mask] += 1.3 * np.sin(np.pi * (t[r_mask] - offset) / 0.08)
    
    return t, ecg

def generate_av_block_first_degree(duration=2):
    """Generate first-degree AV block"""
    samples = int(duration * 1000)
    t = np.linspace(0, duration, samples)
    ecg = np.zeros(samples)
    
    beat_interval = 0.8
    num_beats = int(duration / beat_interval)
    
    for beat in range(num_beats):
        offset = beat * beat_interval
        
        # P wave
        p_mask = (t >= offset) & (t < offset + 0.1)
        ecg[p_mask] += 0.15 * np.sin(np.pi * (t[p_mask] - offset) / 0.1)
        
        # Prolonged PR interval (>0.13s in dogs)
        # QRS complex
        qrs_start = offset + 0.25  # Prolonged PR
        q_mask = (t >= qrs_start) & (t < qrs_start + 0.03)
        ecg[q_mask] -= 0.1 * np.sin(np.pi * (t[q_mask] - qrs_start) / 0.03)
        
        r_mask = (t >= qrs_start + 0.03) & (t < qrs_start + 0.07)
        ecg[r_mask] += 1.5 * np.sin(np.pi * (t[r_mask] - qrs_start - 0.03) / 0.04)
        
        s_mask = (t >= qrs_start + 0.07) & (t < qrs_start + 0.1)
        ecg[s_mask] -= 0.2 * np.sin(np.pi * (t[s_mask] - qrs_start - 0.07) / 0.03)
        
        # T wave
        t_mask = (t >= qrs_start + 0.15) & (t < qrs_start + 0.3)
        ecg[t_mask] += 0.25 * np.sin(np.pi * (t[t_mask] - qrs_start - 0.15) / 0.15)
    
    return t, ecg

def generate_av_block_second_degree(duration=2):
    """Generate second-degree AV block (Mobitz Type I)"""
    samples = int(duration * 1000)
    t = np.linspace(0, duration, samples)
    ecg = np.zeros(samples)
    
    beat_interval = 0.5
    pr_intervals = [0.15, 0.20, 0.25]  # Progressive prolongation
    
    beat = 0
    offset = 0
    while offset < duration - 0.5:
        pr_index = beat % 4
        
        # P wave
        p_mask = (t >= offset) & (t < offset + 0.1)
        ecg[p_mask] += 0.15 * np.sin(np.pi * (t[p_mask] - offset) / 0.1)
        
        # Dropped QRS every 4th beat
        if pr_index < 3:
            pr_interval = pr_intervals[pr_index]
            qrs_start = offset + pr_interval
            
            q_mask = (t >= qrs_start) & (t < qrs_start + 0.03)
            ecg[q_mask] -= 0.1 * np.sin(np.pi * (t[q_mask] - qrs_start) / 0.03)
            
            r_mask = (t >= qrs_start + 0.03) & (t < qrs_start + 0.07)
            ecg[r_mask] += 1.5 * np.sin(np.pi * (t[r_mask] - qrs_start - 0.03) / 0.04)
            
            s_mask = (t >= qrs_start + 0.07) & (t < qrs_start + 0.1)
            ecg[s_mask] -= 0.2 * np.sin(np.pi * (t[s_mask] - qrs_start - 0.07) / 0.03)
            
            t_mask = (t >= qrs_start + 0.15) & (t < qrs_start + 0.3)
            ecg[t_mask] += 0.25 * np.sin(np.pi * (t[t_mask] - qrs_start - 0.15) / 0.15)
        
        offset += beat_interval
        beat += 1
    
    return t, ecg

def generate_sinus_bradycardia(duration=2):
    """Generate sinus bradycardia"""
    samples = int(duration * 1000)
    t = np.linspace(0, duration, samples)
    ecg = np.zeros(samples)
    
    beat_interval = 1.2  # Slow heart rate
    num_beats = int(duration / beat_interval)
    
    for beat in range(num_beats):
        offset = beat * beat_interval
        
        # Normal morphology, just slower
        p_mask = (t >= offset + 0.05) & (t < offset + 0.15)
        ecg[p_mask] += 0.15 * np.sin(np.pi * (t[p_mask] - offset - 0.05) / 0.1)
        
        q_mask = (t >= offset + 0.2) & (t < offset + 0.23)
        ecg[q_mask] -= 0.1 * np.sin(np.pi * (t[q_mask] - offset - 0.2) / 0.03)
        
        r_mask = (t >= offset + 0.23) & (t < offset + 0.27)
        ecg[r_mask] += 1.5 * np.sin(np.pi * (t[r_mask] - offset - 0.23) / 0.04)
        
        s_mask = (t >= offset + 0.27) & (t < offset + 0.3)
        ecg[s_mask] -= 0.2 * np.sin(np.pi * (t[s_mask] - offset - 0.27) / 0.03)
        
        t_mask = (t >= offset + 0.35) & (t < offset + 0.5)
        ecg[t_mask] += 0.25 * np.sin(np.pi * (t[t_mask] - offset - 0.35) / 0.15)
    
    return t, ecg

def generate_sinus_tachycardia(duration=2):
    """Generate sinus tachycardia"""
    return generate_normal_canine_ecg(duration, heart_rate=200)

def generate_premature_ventricular_contraction(duration=2):
    """Generate PVC pattern"""
    samples = int(duration * 1000)
    t = np.linspace(0, duration, samples)
    ecg = np.zeros(samples)
    
    # Normal beats
    for beat in [0, 2]:
        offset = beat * 0.8
        
        p_mask = (t >= offset + 0.05) & (t < offset + 0.15)
        ecg[p_mask] += 0.15 * np.sin(np.pi * (t[p_mask] - offset - 0.05) / 0.1)
        
        q_mask = (t >= offset + 0.2) & (t < offset + 0.23)
        ecg[q_mask] -= 0.1 * np.sin(np.pi * (t[q_mask] - offset - 0.2) / 0.03)
        
        r_mask = (t >= offset + 0.23) & (t < offset + 0.27)
        ecg[r_mask] += 1.5 * np.sin(np.pi * (t[r_mask] - offset - 0.23) / 0.04)
        
        s_mask = (t >= offset + 0.27) & (t < offset + 0.3)
        ecg[s_mask] -= 0.2 * np.sin(np.pi * (t[s_mask] - offset - 0.27) / 0.03)
        
        t_mask = (t >= offset + 0.35) & (t < offset + 0.5)
        ecg[t_mask] += 0.25 * np.sin(np.pi * (t[t_mask] - offset - 0.35) / 0.15)
    
    # PVC (wide, bizarre, premature)
    offset = 1.2
    pvc_mask = (t >= offset) & (t < offset + 0.2)
    ecg[pvc_mask] += 2.0 * np.sin(np.pi * (t[pvc_mask] - offset) / 0.2)
    ecg[pvc_mask] += 0.8 * np.sin(3 * np.pi * (t[pvc_mask] - offset) / 0.2)
    
    # Compensatory pause after PVC
    
    return t, ecg

def generate_supraventricular_tachycardia(duration=2):
    """Generate supraventricular tachycardia (SVT)"""
    samples = int(duration * 1000)
    t = np.linspace(0, duration, samples)
    ecg = np.zeros(samples)
    
    beat_interval = 0.25  # Very fast but regular
    num_beats = int(duration / beat_interval)
    
    for beat in range(num_beats):
        offset = beat * beat_interval
        
        # P waves may be buried in QRS or T waves
        p_mask = (t >= offset) & (t < offset + 0.05)
        ecg[p_mask] += 0.08 * np.sin(np.pi * (t[p_mask] - offset) / 0.05)
        
        # Narrow QRS complex
        q_mask = (t >= offset + 0.06) & (t < offset + 0.08)
        ecg[q_mask] -= 0.08 * np.sin(np.pi * (t[q_mask] - offset - 0.06) / 0.02)
        
        r_mask = (t >= offset + 0.08) & (t < offset + 0.11)
        ecg[r_mask] += 1.2 * np.sin(np.pi * (t[r_mask] - offset - 0.08) / 0.03)
        
        s_mask = (t >= offset + 0.11) & (t < offset + 0.13)
        ecg[s_mask] -= 0.15 * np.sin(np.pi * (t[s_mask] - offset - 0.11) / 0.02)
        
        # T wave
        t_mask = (t >= offset + 0.16) & (t < offset + 0.23)
        ecg[t_mask] += 0.2 * np.sin(np.pi * (t[t_mask] - offset - 0.16) / 0.07)
    
    return t, ecg

def generate_sinus_bradycardia(duration=2):
    """Generate sinus bradycardia"""
    samples = int(duration * 1000)
    t = np.linspace(0, duration, samples)
    ecg = np.zeros(samples)
    
    beat_interval = 1.2  # Slow heart rate
    num_beats = int(duration / beat_interval)
    
    for beat in range(num_beats):
        offset = beat * beat_interval
        
        # Normal morphology, just slower
        p_mask = (t >= offset + 0.05) & (t < offset + 0.15)
        ecg[p_mask] += 0.15 * np.sin(np.pi * (t[p_mask] - offset - 0.05) / 0.1)
        
        q_mask = (t >= offset + 0.2) & (t < offset + 0.23)
        ecg[q_mask] -= 0.1 * np.sin(np.pi * (t[q_mask] - offset - 0.2) / 0.03)
        
        r_mask = (t >= offset + 0.23) & (t < offset + 0.27)
        ecg[r_mask] += 1.5 * np.sin(np.pi * (t[r_mask] - offset - 0.23) / 0.04)
        
        s_mask = (t >= offset + 0.27) & (t < offset + 0.3)
        ecg[s_mask] -= 0.2 * np.sin(np.pi * (t[s_mask] - offset - 0.27) / 0.03)
        
        t_mask = (t >= offset + 0.35) & (t < offset + 0.5)
        ecg[t_mask] += 0.25 * np.sin(np.pi * (t[t_mask] - offset - 0.35) / 0.15)
    
    return t, ecg

def generate_sinus_tachycardia(duration=2):
    """Generate sinus tachycardia"""
    return generate_normal_canine_ecg(duration, heart_rate=200)

def generate_sinus_arrhythmia(duration=2):
    """Generate sinus arrhythmia (common in dogs)"""
    samples = int(duration * 1000)
    t = np.linspace(0, duration, samples)
    ecg = np.zeros(samples)
    
    # Variable R-R intervals (respiratory variation)
    beat_intervals = [0.6, 0.7, 0.8, 0.75, 0.65]
    
    beat = 0
    offset = 0
    while offset < duration - 0.5:
        interval_index = beat % len(beat_intervals)
        
        # P wave
        p_mask = (t >= offset + 0.05) & (t < offset + 0.15)
        ecg[p_mask] += 0.15 * np.sin(np.pi * (t[p_mask] - offset - 0.05) / 0.1)
        
        # QRS complex
        q_mask = (t >= offset + 0.2) & (t < offset + 0.23)
        ecg[q_mask] -= 0.1 * np.sin(np.pi * (t[q_mask] - offset - 0.2) / 0.03)
        
        r_mask = (t >= offset + 0.23) & (t < offset + 0.27)
        ecg[r_mask] += 1.5 * np.sin(np.pi * (t[r_mask] - offset - 0.23) / 0.04)
        
        s_mask = (t >= offset + 0.27) & (t < offset + 0.3)
        ecg[s_mask] -= 0.2 * np.sin(np.pi * (t[s_mask] - offset - 0.27) / 0.03)
        
        # T wave
        t_mask = (t >= offset + 0.35) & (t < offset + 0.5)
        ecg[t_mask] += 0.25 * np.sin(np.pi * (t[t_mask] - offset - 0.35) / 0.15)
        
        offset += beat_intervals[interval_index]
        beat += 1
    
    return t, ecg

def generate_ventricular_fibrillation(duration=2):
    """Generate ventricular fibrillation"""
    samples = int(duration * 1000)
    t = np.linspace(0, duration, samples)
    
    # Chaotic, irregular waveform
    ecg = 0.8 * np.random.randn(samples)
    
    # Add some higher frequency components
    for freq in [8, 12, 15, 20]:
        phase = np.random.rand() * 2 * np.pi
        amplitude = np.random.uniform(0.3, 0.7)
        ecg += amplitude * np.sin(2 * np.pi * freq * t + phase)
    
    return t, ecg

def generate_asystole(duration=2):
    """Generate asystole (flat line)"""
    samples = int(duration * 1000)
    t = np.linspace(0, duration, samples)
    
    # Essentially flat with minimal noise
    ecg = 0.02 * np.random.randn(samples)
    
    return t, ecg

def generate_left_bundle_branch_block(duration=2):
    """Generate left bundle branch block (LBBB)"""
    samples = int(duration * 1000)
    t = np.linspace(0, duration, samples)
    ecg = np.zeros(samples)
    
    beat_interval = 0.8
    num_beats = int(duration / beat_interval)
    
    for beat in range(num_beats):
        offset = beat * beat_interval
        
        # Normal P wave
        p_mask = (t >= offset + 0.05) & (t < offset + 0.15)
        ecg[p_mask] += 0.15 * np.sin(np.pi * (t[p_mask] - offset - 0.05) / 0.1)
        
        # Wide QRS complex (>0.08s) with notched R wave
        q_mask = (t >= offset + 0.2) & (t < offset + 0.23)
        ecg[q_mask] -= 0.05 * np.sin(np.pi * (t[q_mask] - offset - 0.2) / 0.03)
        
        # Notched, prolonged R wave
        r_mask = (t >= offset + 0.23) & (t < offset + 0.35)
        ecg[r_mask] += 1.4 * np.sin(np.pi * (t[r_mask] - offset - 0.23) / 0.12)
        ecg[r_mask] += 0.3 * np.sin(3 * np.pi * (t[r_mask] - offset - 0.23) / 0.12)
        
        # T wave (often opposite direction)
        t_mask = (t >= offset + 0.4) & (t < offset + 0.55)
        ecg[t_mask] -= 0.2 * np.sin(np.pi * (t[t_mask] - offset - 0.4) / 0.15)
    
    return t, ecg

def generate_right_bundle_branch_block(duration=2):
    """Generate right bundle branch block (RBBB)"""
    samples = int(duration * 1000)
    t = np.linspace(0, duration, samples)
    ecg = np.zeros(samples)
    
    beat_interval = 0.8
    num_beats = int(duration / beat_interval)
    
    for beat in range(num_beats):
        offset = beat * beat_interval
        
        # Normal P wave
        p_mask = (t >= offset + 0.05) & (t < offset + 0.15)
        ecg[p_mask] += 0.15 * np.sin(np.pi * (t[p_mask] - offset - 0.05) / 0.1)
        
        # Wide QRS with RSR' pattern
        r_mask = (t >= offset + 0.2) & (t < offset + 0.25)
        ecg[r_mask] += 0.8 * np.sin(np.pi * (t[r_mask] - offset - 0.2) / 0.05)
        
        s_mask = (t >= offset + 0.25) & (t < offset + 0.28)
        ecg[s_mask] -= 0.4 * np.sin(np.pi * (t[s_mask] - offset - 0.25) / 0.03)
        
        # R' (second R wave)
        r2_mask = (t >= offset + 0.28) & (t < offset + 0.35)
        ecg[r2_mask] += 1.2 * np.sin(np.pi * (t[r2_mask] - offset - 0.28) / 0.07)
        
        # T wave
        t_mask = (t >= offset + 0.4) & (t < offset + 0.55)
        ecg[t_mask] += 0.25 * np.sin(np.pi * (t[t_mask] - offset - 0.4) / 0.15)
    
    return t, ecg

def generate_hyperkalemia(duration=2):
    """Generate hyperkalemia pattern"""
    samples = int(duration * 1000)
    t = np.linspace(0, duration, samples)
    ecg = np.zeros(samples)
    
    beat_interval = 0.8
    num_beats = int(duration / beat_interval)
    
    for beat in range(num_beats):
        offset = beat * beat_interval
        
        # Tall, peaked T waves
        # Flattened or absent P waves
        p_mask = (t >= offset + 0.05) & (t < offset + 0.15)
        ecg[p_mask] += 0.05 * np.sin(np.pi * (t[p_mask] - offset - 0.05) / 0.1)
        
        # Widened QRS
        q_mask = (t >= offset + 0.2) & (t < offset + 0.24)
        ecg[q_mask] -= 0.1 * np.sin(np.pi * (t[q_mask] - offset - 0.2) / 0.04)
        
        r_mask = (t >= offset + 0.24) & (t < offset + 0.3)
        ecg[r_mask] += 1.5 * np.sin(np.pi * (t[r_mask] - offset - 0.24) / 0.06)
        
        s_mask = (t >= offset + 0.3) & (t < offset + 0.34)
        ecg[s_mask] -= 0.2 * np.sin(np.pi * (t[s_mask] - offset - 0.3) / 0.04)
        
        # Tall, peaked, narrow T wave
        t_mask = (t >= offset + 0.4) & (t < offset + 0.5)
        ecg[t_mask] += 0.8 * np.sin(np.pi * (t[t_mask] - offset - 0.4) / 0.1)
    
    return t, ecg

def generate_hypokalemia(duration=2):
    """Generate hypokalemia pattern"""
    samples = int(duration * 1000)
    t = np.linspace(0, duration, samples)
    ecg = np.zeros(samples)
    
    beat_interval = 0.8
    num_beats = int(duration / beat_interval)
    
    for beat in range(num_beats):
        offset = beat * beat_interval
        
        # P wave
        p_mask = (t >= offset + 0.05) & (t < offset + 0.15)
        ecg[p_mask] += 0.15 * np.sin(np.pi * (t[p_mask] - offset - 0.05) / 0.1)
        
        # QRS complex
        q_mask = (t >= offset + 0.2) & (t < offset + 0.23)
        ecg[q_mask] -= 0.1 * np.sin(np.pi * (t[q_mask] - offset - 0.2) / 0.03)
        
        r_mask = (t >= offset + 0.23) & (t < offset + 0.27)
        ecg[r_mask] += 1.5 * np.sin(np.pi * (t[r_mask] - offset - 0.23) / 0.04)
        
        s_mask = (t >= offset + 0.27) & (t < offset + 0.3)
        ecg[s_mask] -= 0.2 * np.sin(np.pi * (t[s_mask] - offset - 0.27) / 0.03)
        
        # Flattened T wave
        t_mask = (t >= offset + 0.35) & (t < offset + 0.5)
        ecg[t_mask] += 0.08 * np.sin(np.pi * (t[t_mask] - offset - 0.35) / 0.15)
        
        # Prominent U wave (characteristic of hypokalemia)
        u_mask = (t >= offset + 0.52) & (t < offset + 0.65)
        ecg[u_mask] += 0.2 * np.sin(np.pi * (t[u_mask] - offset - 0.52) / 0.13)
    
    return t, ecg

def generate_hypercalcemia(duration=2):
    """Generate hypercalcemia pattern"""
    samples = int(duration * 1000)
    t = np.linspace(0, duration, samples)
    ecg = np.zeros(samples)
    
    beat_interval = 0.8
    num_beats = int(duration / beat_interval)
    
    for beat in range(num_beats):
        offset = beat * beat_interval
        
        # P wave
        p_mask = (t >= offset + 0.05) & (t < offset + 0.15)
        ecg[p_mask] += 0.15 * np.sin(np.pi * (t[p_mask] - offset - 0.05) / 0.1)
        
        # Short QT interval
        # QRS complex
        q_mask = (t >= offset + 0.2) & (t < offset + 0.23)
        ecg[q_mask] -= 0.1 * np.sin(np.pi * (t[q_mask] - offset - 0.2) / 0.03)
        
        r_mask = (t >= offset + 0.23) & (t < offset + 0.27)
        ecg[r_mask] += 1.5 * np.sin(np.pi * (t[r_mask] - offset - 0.23) / 0.04)
        
        s_mask = (t >= offset + 0.27) & (t < offset + 0.3)
        ecg[s_mask] -= 0.2 * np.sin(np.pi * (t[s_mask] - offset - 0.27) / 0.03)
        
        # Shortened ST segment and early T wave
        t_mask = (t >= offset + 0.31) & (t < offset + 0.42)
        ecg[t_mask] += 0.25 * np.sin(np.pi * (t[t_mask] - offset - 0.31) / 0.11)
    
    return t, ecg

def generate_hypocalcemia(duration=2):
    """Generate hypocalcemia pattern"""
    samples = int(duration * 1000)
    t = np.linspace(0, duration, samples)
    ecg = np.zeros(samples)
    
    beat_interval = 0.8
    num_beats = int(duration / beat_interval)
    
    for beat in range(num_beats):
        offset = beat * beat_interval
        
        # P wave
        p_mask = (t >= offset + 0.05) & (t < offset + 0.15)
        ecg[p_mask] += 0.15 * np.sin(np.pi * (t[p_mask] - offset - 0.05) / 0.1)
        
        # QRS complex
        q_mask = (t >= offset + 0.2) & (t < offset + 0.23)
        ecg[q_mask] -= 0.1 * np.sin(np.pi * (t[q_mask] - offset - 0.2) / 0.03)
        
        r_mask = (t >= offset + 0.23) & (t < offset + 0.27)
        ecg[r_mask] += 1.5 * np.sin(np.pi * (t[r_mask] - offset - 0.23) / 0.04)
        
        s_mask = (t >= offset + 0.27) & (t < offset + 0.3)
        ecg[s_mask] -= 0.2 * np.sin(np.pi * (t[s_mask] - offset - 0.27) / 0.03)
        
        # Prolonged ST segment (prolonged QT interval)
        st_mask = (t >= offset + 0.3) & (t < offset + 0.5)
        ecg[st_mask] += 0.05  # Flat ST segment
        
        # Delayed T wave
        t_mask = (t >= offset + 0.5) & (t < offset + 0.65)
        ecg[t_mask] += 0.25 * np.sin(np.pi * (t[t_mask] - offset - 0.5) / 0.15)
    
    return t, ecg

# Dictionary of all ECG patterns
ECG_PATTERNS = {
    'normal_canine': {
        'name': 'Normal Canine ECG',
        'function': generate_normal_canine_ecg,
        'category': 'Normal Rhythms',
        'species': 'Canine'
    },
    'normal_feline': {
        'name': 'Normal Feline ECG',
        'function': generate_normal_feline_ecg,
        'category': 'Normal Rhythms',
        'species': 'Feline'
    },
    'normal_equine': {
        'name': 'Normal Equine ECG',
        'function': generate_normal_equine_ecg,
        'category': 'Normal Rhythms',
        'species': 'Equine'
    },
    'sinus_bradycardia': {
        'name': 'Sinus Bradycardia',
        'function': generate_sinus_bradycardia,
        'category': 'Sinus Rhythms',
        'species': 'All'
    },
    'sinus_tachycardia': {
        'name': 'Sinus Tachycardia',
        'function': generate_sinus_tachycardia,
        'category': 'Sinus Rhythms',
        'species': 'All'
    },
    'sinus_arrhythmia': {
        'name': 'Sinus Arrhythmia',
        'function': generate_sinus_arrhythmia,
        'category': 'Sinus Rhythms',
        'species': 'Canine'
    },
    'atrial_fibrillation': {
        'name': 'Atrial Fibrillation',
        'function': generate_atrial_fibrillation,
        'category': 'Atrial Arrhythmias',
        'species': 'All'
    },
    'atrial_flutter': {
        'name': 'Atrial Flutter',
        'function': generate_atrial_flutter,
        'category': 'Atrial Arrhythmias',
        'species': 'All'
    },
    'svt': {
        'name': 'Supraventricular Tachycardia',
        'function': generate_supraventricular_tachycardia,
        'category': 'Atrial Arrhythmias',
        'species': 'All'
    },
    'pvc': {
        'name': 'Premature Ventricular Contraction',
        'function': generate_premature_ventricular_contraction,
        'category': 'Ventricular Arrhythmias',
        'species': 'All'
    },
    'ventricular_tachycardia': {
        'name': 'Ventricular Tachycardia',
        'function': generate_ventricular_tachycardia,
        'category': 'Ventricular Arrhythmias',
        'species': 'All'
    },
    'ventricular_fibrillation': {
        'name': 'Ventricular Fibrillation',
        'function': generate_ventricular_fibrillation,
        'category': 'Ventricular Arrhythmias',
        'species': 'All'
    },
    'av_block_1st': {
        'name': 'First-Degree AV Block',
        'function': generate_av_block_first_degree,
        'category': 'AV Blocks',
        'species': 'All'
    },
    'av_block_2nd': {
        'name': 'Second-Degree AV Block',
        'function': generate_av_block_second_degree,
        'category': 'AV Blocks',
        'species': 'All'
    },
    'av_block_3rd': {
        'name': 'Third-Degree AV Block',
        'function': generate_av_block_third_degree,
        'category': 'AV Blocks',
        'species': 'All'
    },
    'lbbb': {
        'name': 'Left Bundle Branch Block',
        'function': generate_left_bundle_branch_block,
        'category': 'Conduction Abnormalities',
        'species': 'All'
    },
    'rbbb': {
        'name': 'Right Bundle Branch Block',
        'function': generate_right_bundle_branch_block,
        'category': 'Conduction Abnormalities',
        'species': 'All'
    },
    'hyperkalemia': {
        'name': 'Hyperkalemia',
        'function': generate_hyperkalemia,
        'category': 'Electrolyte Abnormalities',
        'species': 'All'
    },
    'hypokalemia': {
        'name': 'Hypokalemia',
        'function': generate_hypokalemia,
        'category': 'Electrolyte Abnormalities',
        'species': 'All'
    },
    'hypercalcemia': {
        'name': 'Hypercalcemia',
        'function': generate_hypercalcemia,
        'category': 'Electrolyte Abnormalities',
        'species': 'All'
    },
    'hypocalcemia': {
        'name': 'Hypocalcemia',
        'function': generate_hypocalcemia,
        'category': 'Electrolyte Abnormalities',
        'species': 'All'
    },
    'asystole': {
        'name': 'Asystole',
        'function': generate_asystole,
        'category': 'Emergency Rhythms',
        'species': 'All'
    }
}

# Educational content
EDUCATIONAL_CONTENT = {
    'basic': {
        'title': 'Basic ECG Concepts for Veterinary Technicians',
        'sections': [
            {
                'heading': 'What is an ECG?',
                'content': '''
                An electrocardiogram (ECG or EKG) is a diagnostic tool that records the electrical activity 
                of the heart over time. It provides valuable information about heart rate, rhythm, and 
                can help identify various cardiac abnormalities in animals.
                '''
            },
            {
                'heading': 'Why ECGs are Important in Veterinary Medicine',
                'content': '''
                ECGs are essential for:
                • Pre-anesthetic screening
                • Diagnosing arrhythmias
                • Monitoring critically ill patients
                • Evaluating cardiac disease
                • Assessing electrolyte imbalances
                • Monitoring response to treatment
                '''
            },
            {
                'heading': 'Basic ECG Components',
                'content': '''
                <strong>P Wave:</strong> Represents atrial depolarization (atria contracting)
                <br><strong>QRS Complex:</strong> Represents ventricular depolarization (ventricles contracting)
                <br><strong>T Wave:</strong> Represents ventricular repolarization (ventricles relaxing)
                <br><strong>PR Interval:</strong> Time from atrial to ventricular depolarization
                <br><strong>QT Interval:</strong> Total time for ventricular depolarization and repolarization
                '''
            },
            {
                'heading': 'Normal Heart Rates by Species',
                'content': '''
                • <strong>Dogs:</strong> 60-180 beats per minute (varies by size)
                • <strong>Cats:</strong> 120-240 beats per minute
                • <strong>Horses:</strong> 28-50 beats per minute
                • <strong>Small dogs:</strong> Higher rates (100-180 bpm)
                • <strong>Large dogs:</strong> Lower rates (60-120 bpm)
                '''
            },
            {
                'heading': 'Lead Placement Basics',
                'content': '''
                Standard limb leads in veterinary medicine:
                <br>• <strong>RA (Right Arm):</strong> Right forelimb
                <br>• <strong>LA (Left Arm):</strong> Left forelimb
                <br>• <strong>RL (Right Leg):</strong> Right hindlimb
                <br>• <strong>LL (Left Leg):</strong> Left hindlimb
                <br><br>Lead II is most commonly used for rhythm analysis in veterinary medicine.
                '''
            }
        ]
    },
    'intermediate': {
        'title': 'Intermediate ECG Interpretation',
        'sections': [
            {
                'heading': 'Systematic ECG Analysis',
                'content': '''
                Follow these steps for every ECG:
                <br>1. <strong>Rate:</strong> Calculate heart rate (count R waves)
                <br>2. <strong>Rhythm:</strong> Regular or irregular?
                <br>3. <strong>P Waves:</strong> Present? Normal morphology? One P per QRS?
                <br>4. <strong>PR Interval:</strong> Consistent? Normal duration?
                <br>5. <strong>QRS Complex:</strong> Normal width and morphology?
                <br>6. <strong>ST Segment:</strong> Elevated or depressed?
                <br>7. <strong>T Wave:</strong> Normal direction and size?
                '''
            },
            {
                'heading': 'Measuring ECG Intervals',
                'content': '''
                <strong>Normal Values in Dogs (Lead II, 50mm/sec):</strong>
                <br>• P wave duration: < 0.04 seconds (< 2 small boxes)
                <br>• PR interval: 0.06-0.13 seconds
                <br>• QRS duration: < 0.05 seconds (small dogs), < 0.06 seconds (large dogs)
                <br>• QT interval: 0.15-0.25 seconds
                <br><br><strong>Normal Values in Cats:</strong>
                <br>• P wave duration: < 0.04 seconds
                <br>• PR interval: 0.05-0.09 seconds
                <br>• QRS duration: < 0.04 seconds
                <br>• QT interval: 0.12-0.18 seconds
                <br><br><strong>Normal Values in Horses:</strong>
                <br>• P wave duration: 0.08-0.14 seconds
                <br>• PR interval: 0.22-0.56 seconds
                <br>• QRS duration: 0.08-0.14 seconds
                '''
            },
            {
                'heading': 'Common Arrhythmias',
                'content': '''
                <strong>Sinus Arrhythmia:</strong> Normal in dogs, rate varies with respiration
                <br><strong>Sinus Bradycardia:</strong> Slow heart rate, can be normal in athletic dogs or horses
                <br><strong>Sinus Tachycardia:</strong> Fast heart rate, often due to pain, fear, or fever
                <br><strong>Atrial Fibrillation:</strong> Irregularly irregular rhythm, no distinct P waves
                <br><strong>Ventricular Premature Complexes (VPCs):</strong> Early, wide, bizarre QRS complexes
                '''
            },
            {
                'heading': 'Clinical Significance of Arrhythmias',
                'content': '''
                <strong>Benign Arrhythmias:</strong>
                <br>• Sinus arrhythmia in dogs
                <br>• Occasional VPCs in healthy animals
                <br>• Sinus bradycardia in athletic animals
                <br><br><strong>Potentially Serious Arrhythmias:</strong>
                <br>• Atrial fibrillation (especially in small dogs)
                <br>• Ventricular tachycardia
                <br>• Third-degree AV block
                <br>• Frequent or multiform VPCs
                '''
            },
            {
                'heading': 'Species-Specific Considerations',
                'content': '''
                <strong>Dogs:</strong> Sinus arrhythmia is normal and common
                <br><strong>Cats:</strong> Any arrhythmia is potentially significant
                <br><strong>Horses:</strong> Second-degree AV block can be normal at rest
                <br><strong>Brachycephalic breeds:</strong> May have baseline ST segment changes
                <br><strong>Giant breeds:</strong> Prone to atrial fibrillation
                '''
            },
            {
                'heading': 'Artifact Recognition',
                'content': '''
                Common sources of artifact:
                <br>• <strong>Muscle tremor:</strong> Irregular baseline fluctuation
                <br>• <strong>Patient movement:</strong> Large baseline shifts
                <br>• <strong>Poor contact:</strong> Intermittent signal loss
                <br>• <strong>Electrical interference:</strong> 60Hz (AC) interference
                <br>• <strong>Panting/purring:</strong> Rhythmic baseline movement
                <br><br>Always ensure proper technique to minimize artifact.
                '''
            }
        ]
    },
    'advanced': {
        'title': 'Advanced ECG Interpretation',
        'sections': [
            {
                'heading': 'Chamber Enlargement Patterns',
                'content': '''
                <strong>Left Atrial Enlargement (LAE):</strong>
                <br>• P wave duration > 0.04 seconds (dogs), > 0.04 seconds (cats)
                <br>• Notched or bifid P wave ("P mitrale")
                <br>• Common in mitral valve disease
                <br><br><strong>Right Atrial Enlargement (RAE):</strong>
                <br>• Tall, peaked P waves (> 0.4 mV in dogs)
                <br>• "P pulmonale" pattern
                <br>• Associated with pulmonary hypertension
                <br><br><strong>Left Ventricular Enlargement (LVE):</strong>
                <br>• Increased R wave amplitude in Lead II
                <br>• Prolonged QRS duration
                <br>• ST segment depression
                <br><br><strong>Right Ventricular Enlargement (RVE):</strong>
                <br>• Deep S waves in leads I, II, III, aVF
                <br>• Right axis deviation
                <br>• Associated with pulmonic stenosis, heartworm disease
                '''
            },
            {
                'heading': 'Electrolyte Abnormalities',
                'content': '''
                <strong>Hyperkalemia (High Potassium):</strong>
                <br>• Peaked, narrow T waves
                <br>• Prolonged PR interval
                <br>• Widened QRS complex
                <br>• Flattened or absent P waves (severe cases)
                <br>• Can lead to cardiac arrest - EMERGENCY
                <br><br><strong>Hypokalemia (Low Potassium):</strong>
                <br>• ST segment depression
                <br>• Flattened T waves
                <br>• Prominent U waves
                <br>• Prolonged QT interval
                <br><br><strong>Hypercalcemia (High Calcium):</strong>
                <br>• Shortened QT interval
                <br>• Shortened ST segment
                <br><br><strong>Hypocalcemia (Low Calcium):</strong>
                <br>• Prolonged QT interval
                <br>• Prolonged ST segment
                <br>• Associated with eclampsia, ethylene glycol toxicity
                '''
            },
            {
                'heading': 'AV Block Classification',
                'content': '''
                <strong>First-Degree AV Block:</strong>
                <br>• Prolonged PR interval (> 0.13s in dogs, > 0.09s in cats)
                <br>• Every P wave conducted
                <br>• Usually benign
                <br><br><strong>Second-Degree AV Block:</strong>
                <br>• <em>Mobitz Type I (Wenckebach):</em> Progressive PR prolongation, then dropped QRS
                <br>• <em>Mobitz Type II:</em> Constant PR interval with intermittent dropped QRS
                <br>• Can be normal in horses and athletic dogs at rest
                <br><br><strong>Third-Degree (Complete) AV Block:</strong>
                <br>• Complete dissociation between P waves and QRS complexes
                <br>• Atrial and ventricular rhythms independent
                <br>• Requires pacemaker in symptomatic animals
                <br>• EMERGENCY if causing collapse/weakness
                '''
            },
            {
                'heading': 'Bundle Branch Blocks',
                'content': '''
                <strong>Left Bundle Branch Block (LBBB):</strong>
                <br>• Wide QRS complex (> 0.08s)
                <br>• Positive (upward) QRS in leads I, II, III, aVF
                <br>• Notched R wave
                <br>• Associated with cardiomyopathy, severe left ventricular disease
                <br><br><strong>Right Bundle Branch Block (RBBB):</strong>
                <br>• Wide QRS complex (> 0.08s)
                <br>• RSR' pattern (M-shaped QRS)
                <br>• Deep S wave in lead I
                <br>• Can be normal variant or associated with right heart disease
                '''
            },
            {
                'heading': 'Ventricular Arrhythmia Grading',
                'content': '''
                <strong>Lown Grading System (Modified for Veterinary):</strong>
                <br>• Grade 0: No VPCs
                <br>• Grade 1: Occasional isolated VPCs (< 30/hour)
                <br>• Grade 2: Frequent isolated VPCs (> 30/hour)
                <br>• Grade 3: Multiform VPCs
                <br>• Grade 4A: Couplets (2 consecutive VPCs)
                <br>• Grade 4B: Ventricular tachycardia (≥3 consecutive VPCs)
                <br>• Grade 5: R-on-T phenomenon (VPC on T wave)
                <br><br>Higher grades indicate increased risk and may require antiarrhythmic therapy.
                '''
            },
            {
                'heading': 'Emergency Rhythms Recognition',
                'content': '''
                <strong>Ventricular Fibrillation:</strong>
                <br>• Chaotic, irregular waveform with no discernible QRS complexes
                <br>• No cardiac output - IMMEDIATE defibrillation required
                <br>• CPR in progress
                <br><br><strong>Ventricular Tachycardia:</strong>
                <br>• ≥3 consecutive wide QRS complexes at rapid rate (>100 bpm in dogs)
                <br>• May deteriorate to ventricular fibrillation
                <br>• Requires immediate treatment if sustained
                <br><br><strong>Asystole:</strong>
                <br>• Flat line, no electrical activity
                <br>• No cardiac output
                <br>• Begin CPR immediately, check lead connections
                '''
            },
            {
                'heading': 'Drug Effects on ECG',
                'content': '''
                <strong>Digoxin:</strong>
                <br>• ST segment depression ("scooping")
                <br>• Prolonged PR interval
                <br>• Can cause various arrhythmias in toxicity
                <br><br><strong>Quinidine/Procainamide:</strong>
                <br>• Prolonged QRS duration
                <br>• Prolonged QT interval
                <br><br><strong>Beta-blockers:</strong>
                <br>• Sinus bradycardia
                <br>• Prolonged PR interval
                <br>• May cause AV block
                <br><br><strong>Calcium Channel Blockers:</strong>
                <br>• Sinus bradycardia
                <br>• Prolonged PR interval
                <br><br><strong>Anesthetic Agents:</strong>
                <br>• Alpha-2 agonists: Sinus bradycardia, AV blocks
                <br>• Halothane: Sensitizes myocardium to catecholamines
                '''
            },
            {
                'heading': 'Mean Electrical Axis (MEA)',
                'content': '''
                The MEA represents the average direction of ventricular depolarization.
                <br><br><strong>Normal MEA Values:</strong>
                <br>• Dogs: +40° to +100°
                <br>• Cats: 0° to +160°
                <br><br><strong>Axis Deviations:</strong>
                <br>• Left axis deviation: Suggests left ventricular enlargement
                <br>• Right axis deviation: Suggests right ventricular enlargement
                <br>• Extreme axis deviation: May indicate severe chamber enlargement
                <br><br>Calculated using leads I and aVF amplitudes.
                '''
            },
            {
                'heading': 'Breed-Specific Variations',
                'content': '''
                <strong>Boxers:</strong>
                <br>• Prone to arrhythmogenic right ventricular cardiomyopathy (ARVC)
                <br>• Frequent VPCs, ventricular tachycardia
                <br><br><strong>Doberman Pinschers:</strong>
                <br>• Dilated cardiomyopathy (DCM)
                <br>• Atrial fibrillation, ventricular arrhythmias
                <br><br><strong>Cavalier King Charles Spaniels:</strong>
                <br>• Mitral valve disease
                <br>• Left atrial enlargement patterns
                <br><br><strong>German Shepherds:</strong>
                <br>• May have deep Q waves normally
                <br>• Prone to hemangiosarcoma (arrhythmias)
                <br><br><strong>Giant Breeds (Great Danes, Irish Wolfhounds):</strong>
                <br>• Atrial fibrillation common
                <br>• DCM predisposition
                '''
            }
        ]
    }
}

# Detailed waveform descriptions
WAVEFORM_DESCRIPTIONS = {
    'p_wave': {
        'name': 'P Wave',
        'description': 'Represents atrial depolarization',
        'details': '''
        <strong>Normal Characteristics:</strong>
        <br>• Shape: Rounded, upright in Lead II
        <br>• Duration: < 0.04 seconds (< 2 small boxes at 50mm/sec)
        <br>• Amplitude: < 0.4 mV in dogs, < 0.2 mV in cats
        <br><br><strong>Clinical Significance:</strong>
        <br>• Absent P waves: Atrial fibrillation, junctional rhythm, ventricular rhythm
        <br>• Tall P waves: Right atrial enlargement
        <br>• Wide/notched P waves: Left atrial enlargement
        <br>• Variable P wave morphology: Wandering pacemaker
        '''
    },
    'pr_interval': {
        'name': 'PR Interval',
        'description': 'Time from beginning of P wave to beginning of QRS complex',
        'details': '''
        <strong>Normal Values:</strong>
        <br>• Dogs: 0.06-0.13 seconds
        <br>• Cats: 0.05-0.09 seconds
        <br>• Horses: 0.22-0.56 seconds
        <br><br><strong>Clinical Significance:</strong>
        <br>• Prolonged PR: First-degree AV block, hyperkalemia, drug effects
        <br>• Short PR: Pre-excitation syndromes (rare in animals)
        <br>• Variable PR: Second-degree AV block (Mobitz I), third-degree AV block
        '''
    },
    'qrs_complex': {
        'name': 'QRS Complex',
        'description': 'Represents ventricular depolarization',
        'details': '''
        <strong>Components:</strong>
        <br>• Q wave: First negative deflection
        <br>• R wave: First positive deflection
        <br>• S wave: Negative deflection after R wave
        <br><br><strong>Normal Duration:</strong>
        <br>• Dogs: < 0.05s (small), < 0.06s (large)
        <br>• Cats: < 0.04 seconds
        <br>• Horses: 0.08-0.14 seconds
        <br><br><strong>Clinical Significance:</strong>
        <br>• Wide QRS: Bundle branch block, ventricular origin, hyperkalemia
        <br>• Tall R waves: Ventricular enlargement
        <br>• Low amplitude: Pericardial effusion, pleural effusion, obesity
        <br>• Bizarre morphology: Ventricular ectopy, severe electrolyte disturbance
        '''
    },
    'st_segment': {
        'name': 'ST Segment',
        'description': 'Period between ventricular depolarization and repolarization',
        'details': '''
        <strong>Normal Characteristics:</strong>
        <br>• Should be isoelectric (at baseline)
        <br>• Measured from end of QRS (J point) to beginning of T wave
        <br><br><strong>Clinical Significance:</strong>
        <br>• ST elevation: Myocardial injury, pericarditis, ventricular aneurysm
        <br>• ST depression: Myocardial ischemia, hypoxia, digoxin effect
        <br>• "Scooping" ST: Digoxin effect
        <br>• Slurred ST: Hyperkalemia, hypocalcemia
        <br><br><strong>Species Variations:</strong>
        <br>• Brachycephalic dogs may have baseline ST changes
        <br>• Cats rarely show ST changes even with cardiac disease
        '''
    },
    't_wave': {
        'name': 'T Wave',
        'description': 'Represents ventricular repolarization',
        'details': '''
        <strong>Normal Characteristics:</strong>
        <br>• Variable in size and direction
        <br>• Can be positive, negative, or biphasic
        <br>• Should be < 25% of R wave amplitude in dogs
        <br><br><strong>Clinical Significance:</strong>
        <br>• Tall, peaked T waves: Hyperkalemia (EMERGENCY)
        <br>• Flattened T waves: Hypokalemia
        <br>• Inverted T waves: Myocardial ischemia (rare in animals)
        <br>• Biphasic T waves: Can be normal in horses
        <br><br><strong>Important Note:</strong>
        <br>T wave morphology is highly variable in animals and should be 
        interpreted in context with other ECG findings and clinical signs.
        '''
    },
    'qt_interval': {
        'name': 'QT Interval',
        'description': 'Total time for ventricular depolarization and repolarization',
        'details': '''
        <strong>Normal Values:</strong>
        <br>• Dogs: 0.15-0.25 seconds (varies with heart rate)
        <br>• Cats: 0.12-0.18 seconds
        <br>• Varies inversely with heart rate
        <br><br><strong>Clinical Significance:</strong>
        <br>• Prolonged QT: Hypocalcemia, hypokalemia, hypothermia, drug effects
        <br>• Shortened QT: Hypercalcemia, digoxin toxicity
        <br>• Very prolonged QT: Risk of torsades de pointes (polymorphic VT)
        <br><br><strong>Correction for Heart Rate:</strong>
        <br>QTc (corrected) = QT / √RR interval
        <br>Used to account for heart rate variations
        '''
    },
    'u_wave': {
        'name': 'U Wave',
        'description': 'Small deflection sometimes seen after T wave',
        'details': '''
        <strong>Characteristics:</strong>
        <br>• Small, rounded wave following T wave
        <br>• Same polarity as T wave
        <br>• Not always present
        <br><br><strong>Clinical Significance:</strong>
        <br>• Prominent U waves: Hypokalemia (classic finding)
        <br>• May be confused with P wave if close together
        <br>• Can indicate repolarization abnormalities
        <br><br><strong>Veterinary Relevance:</strong>
        <br>Most commonly seen in hypokalemic cats and dogs
        '''
    },
    'rr_interval': {
        'name': 'RR Interval',
        'description': 'Time between consecutive R waves',
        'details': '''
        <strong>Measurement:</strong>
        <br>• Distance from one R wave peak to the next
        <br>• Used to calculate heart rate
        <br>• Heart Rate (bpm) = 3000 / RR interval (in small boxes at 50mm/sec)
        <br><br><strong>Clinical Significance:</strong>
        <br>• Regular RR intervals: Sinus rhythm, atrial flutter
        <br>• Regularly irregular: Second-degree AV block (Mobitz II)
        <br>• Irregularly irregular: Atrial fibrillation, frequent ectopy
        <br>• Variable RR with respiration: Sinus arrhythmia (normal in dogs)
        '''
    }
}

def plot_ecg(t, ecg, title):
    """Generate ECG plot and return as base64 encoded image"""
    fig, ax = plt.subplots(figsize=(12, 4))
    
    # Create ECG grid background
    ax.set_facecolor('#fff5f5')
    ax.grid(True, which='major', color='#ff9999', linewidth=0.8, alpha=0.6)
    ax.grid(True, which='minor', color='#ffcccc', linewidth=0.4, alpha=0.4)
    ax.minorticks_on()
    
    # Plot ECG
    ax.plot(t, ecg, 'r-', linewidth=1.5, label='ECG Signal')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Time (seconds)', fontsize=11)
    ax.set_ylabel('Amplitude (mV)', fontsize=11)
    ax.legend(loc='upper right')
    
    # Set grid intervals to mimic ECG paper
    ax.set_xlim([0, max(t)])
    
    plt.tight_layout()
    
    # Convert plot to base64 string
    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode()
    plt.close(fig)
    
    return image_base64

# Flask routes
@app.route('/')
def index():
    """Main page with navigation"""
    return render_template_string(INDEX_HTML)

@app.route('/waveforms')
def waveforms():
    """Page showing all ECG waveform types"""
    categories = {}
    for key, pattern in ECG_PATTERNS.items():
        category = pattern['category']
        if category not in categories:
            categories[category] = []
        categories[category].append({
            'key': key,
            'name': pattern['name'],
            'species': pattern['species']
        })
    
    return render_template_string(WAVEFORMS_HTML, categories=categories)

@app.route('/education/<level>')
def education(level):
    """Educational content pages"""
    if level in EDUCATIONAL_CONTENT:
        content = EDUCATIONAL_CONTENT[level]
        return render_template_string(EDUCATION_HTML, content=content, level=level)
    return "Content not found", 404

@app.route('/waveform-details')
def waveform_details():
    """Detailed information about ECG wave components"""
    return render_template_string(WAVEFORM_DETAILS_HTML, waveforms=WAVEFORM_DESCRIPTIONS)

@app.route('/api/ecg/<pattern_key>')
def get_ecg(pattern_key):
    """API endpoint to get ECG data"""
    if pattern_key in ECG_PATTERNS:
        pattern = ECG_PATTERNS[pattern_key]
        t, ecg = pattern['function']()
        
        # Generate plot
        image_base64 = plot_ecg(t, ecg, pattern['name'])
        
        return jsonify({
            'success': True,
            'name': pattern['name'],
            'category': pattern['category'],
            'species': pattern['species'],
            'image': image_base64
        })
    
    return jsonify({'success': False, 'error': 'Pattern not found'}), 404

@app.route('/quiz')
def quiz():
    """Interactive quiz page"""
    return render_template_string(QUIZ_HTML)

@app.route('/api/quiz/random')
def random_quiz_question():
    """Generate random quiz question"""
    import random
    
    pattern_key = random.choice(list(ECG_PATTERNS.keys()))
    pattern = ECG_PATTERNS[pattern_key]
    t, ecg = pattern['function']()
    
    # Generate plot without title for quiz
    image_base64 = plot_ecg(t, ecg, "Identify this ECG pattern")
    
    # Generate wrong answers
    all_patterns = list(ECG_PATTERNS.keys())
    all_patterns.remove(pattern_key)
    wrong_answers = random.sample(all_patterns, min(3, len(all_patterns)))
    
    options = [pattern['name']] + [ECG_PATTERNS[key]['name'] for key in wrong_answers]
    random.shuffle(options)
    
    return jsonify({
        'image': image_base64,
        'options': options,
        'correct_answer': pattern['name'],
        'category': pattern['category'],
        'species': pattern['species']
    })

# HTML Templates
# Create templates folder and add these files

# templates/index.html
INDEX_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Veterinary ECG Learning Platform</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        header {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 30px;
            text-align: center;
        }
        
        h1 {
            color: #667eea;
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .subtitle {
            color: #666;
            font-size: 1.2em;
        }
        
        .nav-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 25px;
            margin-top: 30px;
        }
        
        .nav-card {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            text-decoration: none;
            color: inherit;
            transition: transform 0.3s, box-shadow 0.3s;
            cursor: pointer;
        }
        
        .nav-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .nav-card-icon {
            font-size: 3em;
            margin-bottom: 15px;
        }
        
        .nav-card h2 {
            color: #667eea;
            margin-bottom: 10px;
            font-size: 1.5em;
        }
        
        .nav-card p {
            color: #666;
            line-height: 1.6;
        }
        
        .level-badge {
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: bold;
            margin-top: 10px;
        }
        
        .basic { background: #d4edda; color: #155724; }
        .intermediate { background: #fff3cd; color: #856404; }
        .advanced { background: #f8d7da; color: #721c24; }
        
        footer {
            text-align: center;
            color: white;
            margin-top: 50px;
            padding: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🫀 Veterinary ECG Learning Platform</h1>
            <p class="subtitle">Comprehensive ECG Education for Veterinary Technicians</p>
        </header>
        
        <div class="nav-grid">
            <a href="/education/basic" class="nav-card">
                <div class="nav-card-icon">📚</div>
                <h2>Basic ECG Concepts</h2>
                <p>Learn the fundamentals of ECG interpretation, wave components, and normal values for different species.</p>
                <span class="level-badge basic">BASIC</span>
            </a>
            
            <a href="/education/intermediate" class="nav-card">
                <div class="nav-card-icon">📊</div>
                <h2>Intermediate Interpretation</h2>
                <p>Systematic ECG analysis, common arrhythmias, and species-specific considerations.</p>
                <span class="level-badge intermediate">INTERMEDIATE</span>
            </a>
            
            <a href="/education/advanced" class="nav-card">
                <div class="nav-card-icon">🔬</div>
                <h2>Advanced Topics</h2>
                <p>Chamber enlargement, electrolyte abnormalities, conduction blocks, and emergency rhythms.</p>
                <span class="level-badge advanced">ADVANCED</span>
            </a>
            
            <a href="/waveforms" class="nav-card">
                <div class="nav-card-icon">📈</div>
                <h2>ECG Waveform Library</h2>
                <p>Browse and study all types of ECG patterns organized by category and species.</p>
            </a>
            
            <a href="/waveform-details" class="nav-card">
                <div class="nav-card-icon">🔍</div>
                <h2>Wave Component Details</h2>
                <p>Detailed information about P waves, QRS complexes, T waves, and all ECG intervals.</p>
            </a>
            
            <a href="/quiz" class="nav-card">
                <div class="nav-card-icon">🎯</div>
                <h2>Interactive Quiz</h2>
                <p>Test your knowledge with randomly generated ECG patterns and immediate feedback.</p>
            </a>
        </div>
        
        <footer>
            <p>© 2024 Veterinary ECG Learning Platform | Educational Tool for Veterinary Technicians</p>
            <p style="margin-top: 10px; font-size: 0.9em;">Always consult with a licensed veterinarian for clinical interpretation</p>
        </footer>
    </div>
</body>
</html>
'''

# templates/education.html
EDUCATION_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ content.title }}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1000px;
            margin: 0 auto;
        }
        
        .back-button {
            display: inline-block;
            background: white;
            color: #667eea;
            padding: 10px 20px;
            border-radius: 25px;
            text-decoration: none;
            margin-bottom: 20px;
            font-weight: bold;
            transition: transform 0.2s;
        }
        
        .back-button:hover {
            transform: translateX(-5px);
        }
        
        header {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 30px;
        }
        
        h1 {
            color: #667eea;
            font-size: 2.2em;
            margin-bottom: 10px;
        }
        
        .level-indicator {
            display: inline-block;
            padding: 8px 20px;
            border-radius: 25px;
            font-weight: bold;
            text-transform: uppercase;
            font-size: 0.9em;
        }
        
        .basic-level { background: #d4edda; color: #155724; }
        .intermediate-level { background: #fff3cd; color: #856404; }
        .advanced-level { background: #f8d7da; color: #721c24; }
        
        .content-section {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            margin-bottom: 25px;
        }
        
        .content-section h2 {
            color: #667eea;
            font-size: 1.8em;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }
        
        .content-section p, .content-section ul {
            color: #333;
            line-height: 1.8;
            font-size: 1.05em;
        }
        
        .content-section ul {
            margin-left: 20px;
            margin-top: 10px;
        }
        
        .content-section li {
            margin-bottom: 8px;
        }
        
        strong {
            color: #764ba2;
        }
        
        .navigation-buttons {
            display: flex;
            justify-content: space-between;
            margin-top: 30px;
        }
        
        .nav-btn {
            background: white;
            color: #667eea;
            padding: 12px 25px;
            border-radius: 25px;
            text-decoration: none;
            font-weight: bold;
            transition: all 0.3s;
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        }
        
        .nav-btn:hover {
            background: #667eea;
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
    </style>
</head>
<body>
    <div class="container">
        <a href="/" class="back-button">← Back to Home</a>
        
        <header>
            <h1>{{ content.title }}</h1>
            <span class="level-indicator {{ level }}-level">{{ level }} Level</span>
        </header>
        
        {% for section in content.sections %}
        <div class="content-section">
            <h2>{{ section.heading }}</h2>
            <div>{{ section.content | safe }}</div>
        </div>
        {% endfor %}
        
        <div class="navigation-buttons">
            {% if level == 'basic' %}
            <a href="/education/intermediate" class="nav-btn">Next: Intermediate Level →</a>
            {% elif level == 'intermediate' %}
            <a href="/education/basic" class="nav-btn">← Previous: Basic Level</a>
            <a href="/education/advanced" class="nav-btn">Next: Advanced Level →</a>
            {% elif level == 'advanced' %}
            <a href="/education/intermediate" class="nav-btn">← Previous: Intermediate Level</a>
            {% endif %}
        </div>
    </div>
</body>
</html>
'''

# templates/waveforms.html
WAVEFORMS_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ECG Waveform Library</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .back-button {
            display: inline-block;
            background: white;
            color: #667eea;
            padding: 10px 20px;
            border-radius: 25px;
            text-decoration: none;
            margin-bottom: 20px;
            font-weight: bold;
            transition: transform 0.2s;
        }
        
        .back-button:hover {
            transform: translateX(-5px);
        }
        
        header {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 30px;
            text-align: center;
        }
        
        h1 {
            color: #667eea;
            font-size: 2.5em;
        }
        
        .category-section {
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            margin-bottom: 25px;
        }
        
        .category-title {
            color: #667eea;
            font-size: 1.8em;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }
        
        .waveform-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
        }
        
        .waveform-card {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s;
            border: 2px solid transparent;
        }
        
        .waveform-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.15);
            border-color: #667eea;
        }
        
        .waveform-card h3 {
            color: #764ba2;
            margin-bottom: 10px;
            font-size: 1.2em;
        }
        
        .species-badge {
            display: inline-block;
            padding: 5px 12px;
            border-radius: 15px;
            font-size: 0.85em;
            font-weight: bold;
            background: #e9ecef;
            color: #495057;
        }
        
        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.8);
            overflow: auto;
        }
        
        .modal-content {
            background-color: white;
            margin: 50px auto;
            padding: 30px;
            border-radius: 15px;
            width: 90%;
            max-width: 1000px;
            position: relative;
        }
        
        .close {
            color: #aaa;
            float: right;
            font-size: 35px;
            font-weight: bold;
            cursor: pointer;
            line-height: 20px;
        }
        
        .close:hover {
            color: #000;
        }
        
        .modal-title {
            color: #667eea;
            font-size: 2em;
            margin-bottom: 20px;
        }
        
        .ecg-image {
            width: 100%;
            border-radius: 10px;
            margin-top: 20px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .loading {
            text-align: center;
            padding: 40px;
            font-size: 1.2em;
            color: #667eea;
        }
    </style>
</head>
<body>
    <div class="container">
        <a href="/" class="back-button">← Back to Home</a>
        
        <header>
            <h1>📈 ECG Waveform Library</h1>
            <p style="color: #666; margin-top: 10px;">Click on any waveform to view its ECG pattern</p>
        </header>
        
        {% for category, patterns in categories.items() %}
        <div class="category-section">
            <h2 class="category-title">{{ category }}</h2>
            <div class="waveform-grid">
                {% for pattern in patterns %}
                <div class="waveform-card" onclick="loadECG('{{ pattern.key }}')">
                    <h3>{{ pattern.name }}</h3>
                    <span class="species-badge">{{ pattern.species }}</span>
                </div>
                {% endfor %}
            </div>
        </div>
        {% endfor %}
    </div>
    
    <div id="ecgModal" class="modal">
        <div class="modal-content">
            <span class="close" onclick="closeModal()">&times;</span>
            <h2 class="modal-title" id="modalTitle">Loading...</h2>
            <div id="modalBody" class="loading">Loading ECG pattern...</div>
        </div>
    </div>
    
    <script>
        function loadECG(patternKey) {
            const modal = document.getElementById('ecgModal');
            const modalTitle = document.getElementById('modalTitle');
            const modalBody = document.getElementById('modalBody');
            
            modal.style.display = 'block';
            modalTitle.textContent = 'Loading...';
            modalBody.innerHTML = '<div class="loading">Loading ECG pattern...</div>';
            
            fetch(`/api/ecg/${patternKey}`)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        modalTitle.textContent = data.name;
                        modalBody.innerHTML = `
                            <p><strong>Category:</strong> ${data.category}</p>
                            <p><strong>Species:</strong> ${data.species}</p>
                            <img src="data:image/png;base64,${data.image}" class="ecg-image" alt="${data.name}">
                        `;
                    } else {
                        modalBody.innerHTML = '<p style="color: red;">Error loading ECG pattern</p>';
                    }
                })
                .catch(error => {
                    modalBody.innerHTML = '<p style="color: red;">Error: ' + error.message + '</p>';
                });
        }
        
        function closeModal() {
            document.getElementById('ecgModal').style.display = 'none';
        }
        
        window.onclick = function(event) {
            const modal = document.getElementById('ecgModal');
            if (event.target == modal) {
                modal.style.display = 'none';
            }
        }
    </script>
</body>
</html>
'''

# templates/waveform_details.html
WAVEFORM_DETAILS_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ECG Wave Component Details</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1000px;
            margin: 0 auto;
        }
        
        .back-button {
            display: inline-block;
            background: white;
            color: #667eea;
            padding: 10px 20px;
            border-radius: 25px;
            text-decoration: none;
            margin-bottom: 20px;
            font-weight: bold;
            transition: transform 0.2s;
        }
        
        .back-button:hover {
            transform: translateX(-5px);
        }
        
        header {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 30px;
            text-align: center;
        }
        
        h1 {
            color: #667eea;
            font-size: 2.5em;
        }
        
        .wave-card {
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            margin-bottom: 25px;
        }
        
        .wave-card h2 {
            color: #667eea;
            font-size: 1.8em;
            margin-bottom: 10px;
        }
        
        .wave-description {
            color: #764ba2;
            font-size: 1.1em;
            font-style: italic;
            margin-bottom: 15px;
        }
        
        .wave-details {
            color: #333;
            line-height: 1.8;
            font-size: 1.05em;
        }
        
        strong {
            color: #764ba2;
        }
    </style>
</head>
<body>
    <div class="container">
        <a href="/" class="back-button">← Back to Home</a>
        
        <header>
            <h1>🔍 ECG Wave Component Details</h1>
            <p style="color: #666; margin-top: 10px;">Comprehensive guide to ECG waveform components</p>
        </header>
        
        {% for key, waveform in waveforms.items() %}
        <div class="wave-card">
            <h2>{{ waveform.name }}</h2>
            <p class="wave-description">{{ waveform.description }}</p>
            <div class="wave-details">{{ waveform.details | safe }}</div>
        </div>
        {% endfor %}
    </div>
</body>
</html>
'''

# templates/quiz.html
QUIZ_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ECG Quiz</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1000px;
            margin: 0 auto;
        }
        
        .back-button {
            display: inline-block;
            background: white;
            color: #667eea;
            padding: 10px 20px;
            border-radius: 25px;
            text-decoration: none;
            margin-bottom: 20px;
            font-weight: bold;
            transition: transform 0.2s;
        }
        
        .back-button:hover {
            transform: translateX(-5px);
        }
        
        header {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 30px;
            text-align: center;
        }
        
        h1 {
            color: #667eea;
            font-size: 2.5em;
        }
        
        .score-board {
            background: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            margin-bottom: 25px;
            display: flex;
            justify-content: space-around;
            text-align: center;
        }
        
        .score-item {
            flex: 1;
        }
        
        .score-label {
            color: #666;
            font-size: 0.9em;
            margin-bottom: 5px;
        }
        
        .score-value {
            color: #667eea;
            font-size: 2em;
            font-weight: bold;
        }
        
        .quiz-card {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            margin-bottom: 25px;
        }
        
        .ecg-image {
            width: 100%;
            border-radius: 10px;
            margin-bottom: 25px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .options-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 25px;
        }
        
        .option-button {
            background: #f8f9fa;
            border: 2px solid #dee2e6;
            padding: 15px;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s;
            font-size: 1em;
            font-weight: 500;
        }
        
        .option-button:hover {
            background: #e9ecef;
            border-color: #667eea;
            transform: translateY(-2px);
        }
        
        .option-button.selected {
            background: #667eea;
            color: white;
            border-color: #667eea;
        }
        
        .option-button.correct {
            background: #28a745;
            color: white;
            border-color: #28a745;
        }
        
        .option-button.incorrect {
            background: #dc3545;
            color: white;
            border-color: #dc3545;
        }
        
        .option-button:disabled {
            cursor: not-allowed;
            opacity: 0.7;
        }
        
        .button-group {
            display: flex;
            gap: 15px;
            justify-content: center;
        }
        
        .btn {
            padding: 12px 30px;
            border: none;
            border-radius: 25px;
            font-size: 1.1em;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .btn-primary {
            background: #667eea;
            color: white;
        }
        
        .btn-primary:hover {
            background: #5568d3;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        .btn-secondary {
            background: #6c757d;
            color: white;
        }
        
        .btn-secondary:hover {
            background: #5a6268;
        }
        
        .btn:disabled {
            background: #ccc;
            cursor: not-allowed;
        }
        
        .feedback {
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            font-size: 1.1em;
            text-align: center;
        }
        
        .feedback.correct {
            background: #d4edda;
            color: #155724;
            border: 2px solid #28a745;
        }
        
        .feedback.incorrect {
            background: #f8d7da;
            color: #721c24;
            border: 2px solid #dc3545;
        }
        
        .loading {
            text-align: center;
            padding: 40px;
            font-size: 1.2em;
            color: #667eea;
        }
        
        .info-text {
            color: #666;
            font-size: 0.95em;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <a href="/" class="back-button">← Back to Home</a>
        
        <header>
            <h1>🎯 ECG Identification Quiz</h1>
            <p style="color: #666; margin-top: 10px;">Test your ECG interpretation skills</p>
        </header>
        
        <div class="score-board">
            <div class="score-item">
                <div class="score-label">Correct</div>
                <div class="score-value" id="correctScore">0</div>
            </div>
            <div class="score-item">
                <div class="score-label">Incorrect</div>
                <div class="score-value" id="incorrectScore" style="color: #dc3545;">0</div>
            </div>
            <div class="score-item">
                <div class="score-label">Total</div>
                <div class="score-value" id="totalScore" style="color: #6c757d;">0</div>
            </div>
        </div>
        
        <div class="quiz-card">
            <div id="quizContent" class="loading">Loading question...</div>
            
            <div id="feedbackArea"></div>
            
            <div class="button-group">
                <button class="btn btn-primary" id="submitBtn" onclick="submitAnswer()" disabled>Submit Answer</button>
                <button class="btn btn-secondary" id="nextBtn" onclick="loadNewQuestion()" style="display: none;">Next Question</button>
            </div>
        </div>
    </div>
    
    <script>
        let currentQuestion = null;
        let selectedAnswer = null;
        let correctCount = 0;
        let incorrectCount = 0;
        let totalCount = 0;
        
        function loadNewQuestion() {
            // Reset state
            selectedAnswer = null;
            document.getElementById('feedbackArea').innerHTML = '';
            document.getElementById('submitBtn').style.display = 'inline-block';
            document.getElementById('submitBtn').disabled = true;
            document.getElementById('nextBtn').style.display = 'none';
            document.getElementById('quizContent').innerHTML = '<div class="loading">Loading question...</div>';
            
            fetch('/api/quiz/random')
                .then(response => response.json())
                .then(data => {
                    currentQuestion = data;
                    displayQuestion(data);
                })
                .catch(error => {
                    document.getElementById('quizContent').innerHTML = 
                        '<p style="color: red;">Error loading question: ' + error.message + '</p>';
                });
        }
        
        function displayQuestion(data) {
            let html = `
                <img src="data:image/png;base64,${data.image}" class="ecg-image" alt="ECG Pattern">
                <h3 style="color: #667eea; margin-bottom: 20px;">What ECG pattern is shown above?</h3>
                <div class="options-grid">
            `;
            
            data.options.forEach((option, index) => {
                html += `
                    <button class="option-button" onclick="selectOption('${option}', this)">
                        ${option}
                    </button>
                `;
            });
            
            html += '</div>';
            html += `<p class="info-text"><strong>Category:</strong> ${data.category} | <strong>Species:</strong> ${data.species}</p>`;
            
            document.getElementById('quizContent').innerHTML = html;
        }
        
        function selectOption(answer, button) {
            // Remove previous selection
            document.querySelectorAll('.option-button').forEach(btn => {
                btn.classList.remove('selected');
            });
            
            // Select new option
            button.classList.add('selected');
            selectedAnswer = answer;
            document.getElementById('submitBtn').disabled = false;
        }
        
        function submitAnswer() {
            if (!selectedAnswer) return;
            
            totalCount++;
            const isCorrect = selectedAnswer === currentQuestion.correct_answer;
            
            if (isCorrect) {
                correctCount++;
            } else {
                incorrectCount++;
            }
            
            updateScoreboard();
            
            // Disable all buttons
            document.querySelectorAll('.option-button').forEach(btn => {
                btn.disabled = true;
                if (btn.textContent.trim() === currentQuestion.correct_answer) {
                    btn.classList.add('correct');
                } else if (btn.classList.contains('selected')) {
                    btn.classList.add('incorrect');
                }
            });
            
            // Show feedback
            const feedbackDiv = document.getElementById('feedbackArea');
            if (isCorrect) {
                feedbackDiv.innerHTML = `
                    <div class="feedback correct">
                        <strong>✓ Correct!</strong><br>
                        This is ${currentQuestion.correct_answer}
                    </div>
                `;
            } else {
                feedbackDiv.innerHTML = `
                    <div class="feedback incorrect">
                        <strong>✗ Incorrect</strong><br>
                        The correct answer is: ${currentQuestion.correct_answer}
                    </div>
                `;
            }
            
            // Show next button, hide submit
            document.getElementById('submitBtn').style.display = 'none';
            document.getElementById('nextBtn').style.display = 'inline-block';
        }
        
        function updateScoreboard() {
            document.getElementById('correctScore').textContent = correctCount;
            document.getElementById('incorrectScore').textContent = incorrectCount;
            document.getElementById('totalScore').textContent = totalCount;
        }
        
        // Load first question on page load
        window.onload = function() {
            loadNewQuestion();
        };
    </script>
</body>
</html>
'''

# Save templates to files
import os

def create_templates():
    """Create template files"""
    os.makedirs('templates', exist_ok=True)
    
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(INDEX_HTML)
    
    with open('templates/education.html', 'w', encoding='utf-8') as f:
        f.write(EDUCATION_HTML)
    
    with open('templates/waveforms.html', 'w', encoding='utf-8') as f:
        f.write(WAVEFORMS_HTML)
    
    with open('templates/waveform_details.html', 'w', encoding='utf-8') as f:
        f.write(WAVEFORM_DETAILS_HTML)
    
    with open('templates/quiz.html', 'w', encoding='utf-8') as f:
        f.write(QUIZ_HTML)
    
    print("Templates created successfully!")

if __name__ == '__main__':
    import socket
    
    # Get your local IP address
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    print("\nStarting Veterinary ECG Learning Platform...")
    print(f"Access locally at: http://127.0.0.1:5000")
    print(f"Access from other devices at: http://{local_ip}:5000")
    print("\nFeatures:")
    print("- Basic, Intermediate, and Advanced ECG education")
    print("- Complete ECG waveform library with 20+ patterns")
    print("- Detailed wave component information")
    print("- Interactive quiz with instant feedback")
    print("- Species-specific ECG patterns (Canine, Feline, Equine)")
    print("\nPress Ctrl+C to stop the server\n")
    
    app.run(debug=False, host='0.0.0.0', port=5000)