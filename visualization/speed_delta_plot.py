import matplotlib.pyplot as plt 


def plot_speed_delta (d_ref_norm, d_comp_norm, ref_speed, comp_speed, delta_time, ref_name, comp_name, ref_color, comp_color, circuit_info):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 7), sharex=True,
                                gridspec_kw={'height_ratios': [3, 1]})
    ax1.plot(d_ref_norm, ref_speed, label=ref_name, color=ref_color)
    ax1.plot(d_comp_norm, comp_speed, label=comp_name, color=comp_color)
    ax1.set_ylabel('Speed (km/h)')
    ax1.set_title(f'{ref_name} vs {comp_name} - Speed and cumulative delta')

    ax1.set_ylim(0, 350)
    ax1.legend()
    ax1.grid()

    ax2.plot(d_ref_norm, delta_time, color='black', linewidth=1.5)
    ax2.fill_between(d_ref_norm, delta_time, 0, where=(delta_time < 0), color=ref_color, alpha=0.5)
    ax2.fill_between(d_ref_norm, delta_time, 0, where=(delta_time >= 0), color=comp_color, alpha=0.5)
    ax2.axhline(0, color='gray', linewidth=0.5)
    ax2.set_xlabel('Distance (m)')
    ax2.set_ylabel(f' Delta (s)\n<-{ref_name}  {comp_name}->')
    ax2.grid()

    for _, corner in circuit_info.corners.iterrows():
        txt = f"T{corner['Number']}{corner['Letter']}"
        ax1.axvline(x=corner['Distance'], color='gray', 
                linestyle='--', linewidth=0.5, alpha=0.5)
        ax1.text(corner['Distance'], ax1.get_ylim()[1] * 0.95, 
             txt, rotation=90, va='top', ha='right', 
             fontsize=8, color='gray')

    ref_dis_norm_tot = d_ref_norm.max()
    comp_dis_norm_tot = d_comp_norm.max()

    ax1.axvline(x=ref_dis_norm_tot, color=ref_color, linestyle='--', linewidth=1, alpha=1)
    ax1.axvline(x=comp_dis_norm_tot, color=comp_color, linestyle='--', linewidth=1, alpha=1)
    ax2.axhline(y=delta_time[-1], color='blue', linestyle='--', linewidth=1, label=f'Final Delta : {delta_time[-1]:.3f}s')
    ax2.legend(loc='lower left')

    plt.tight_layout()
    return fig