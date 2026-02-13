from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import AntibioticEntry, Egasp_Data
import re

# original post_save function fails during raw_upload
def determine_ris(value, r_breakpoint, i_breakpoint, s_breakpoint, sdd_breakpoint, is_disk=False):
    # Ensure value and at least one of the breakpoints are provided
    if value is not None and (r_breakpoint is not None or s_breakpoint is not None or i_breakpoint is not None or sdd_breakpoint is not None):
         # Convert breakpoint values from string to numbers
        try:
            value = int(value) if is_disk else float(value)  # Convert to int for disk, float otherwise
        except ValueError:
            return None  # Handle cases where the value cannot be converted

        # Check if the intermediate breakpoint is a range (e.g., "24-27")
        if i_breakpoint is not None:
            try:
                if "-" in str(i_breakpoint):
                    lower, upper = map(int if is_disk else float, str(i_breakpoint).split("-"))
                    if lower <= value <= upper:
                        return "I"
                else:
                    i_breakpoint = int(i_breakpoint) if is_disk and i_breakpoint and i_breakpoint.strip().isdigit() else float(i_breakpoint) if i_breakpoint else None
                    if value == i_breakpoint:
                        return "I"
            except ValueError:
                pass

      # For SDD breakpoint
        if sdd_breakpoint is not None:
            try:
                sdd_breakpoint = int(sdd_breakpoint) if is_disk and sdd_breakpoint and sdd_breakpoint.strip().isdigit() else float(sdd_breakpoint) if sdd_breakpoint else None
            except ValueError:
                return None  # Return None if conversion fails
            
            if value == sdd_breakpoint:
                return "SDD"

            
        # If both r_breakpoint and s_breakpoint are provided, compare the value
        if r_breakpoint is not None and s_breakpoint is not None:
            try:
                r_breakpoint = int(r_breakpoint) if is_disk and r_breakpoint and r_breakpoint.strip().isdigit() else float(r_breakpoint) if r_breakpoint else None
                s_breakpoint = int(s_breakpoint) if is_disk and s_breakpoint and s_breakpoint.strip().isdigit() else float(s_breakpoint) if s_breakpoint else None
            except ValueError:
                return None  # Handle cases where the breakpoints cannot be converted
            if is_disk:
                if value <= r_breakpoint:
                    return "R"  
                elif value >= s_breakpoint:
                    return "S" 
                else:
                    return "I"  # Intermediate if value is between the two breakpoints
            else:
                if value >= r_breakpoint: # if MIC antibiotic
                    return "R"
                elif value <= s_breakpoint:
                    return "S"
                else:
                    return "I"
            
        # If only s_breakpoint is provided, use it for comparison
        if s_breakpoint is not None:
            try:
                 s_breakpoint = int(s_breakpoint) if is_disk and s_breakpoint and s_breakpoint.strip().isdigit() else float(s_breakpoint) if s_breakpoint else None
            except ValueError:
                return None  # Handle cases where the breakpoint cannot be converted
            if is_disk:
                if value >= s_breakpoint:
                    return "S"  
                else:
                    return "R"
            else:
                if value <= s_breakpoint: #if MIC antibiotic
                    return "S"
                else:
                    return "R"
        # If only r_breakpoint is provided, use it for comparison
        if r_breakpoint is not None:
            try:
                 r_breakpoint = int(r_breakpoint) if is_disk and r_breakpoint and r_breakpoint.strip().isdigit() else float(r_breakpoint) if r_breakpoint else None
            except ValueError:
                return None  # Handle cases where the breakpoint cannot be converted
            if is_disk:
                if value <= r_breakpoint:
                    return "R"  
                else:
                    return "S"
            else:
                if value >= r_breakpoint: #if MIC antibiotic
                    return "R"
                else:
                    return "S"

        return None  # Return None if no valid interpretation can be made


@receiver(post_save, sender=AntibioticEntry)
def update_ris_interpretation(sender, instance, **kwargs):
    updated_fields = []

    # Retrieve the BreakpointsTable entry associated with the AntibioticEntry
    breakpoint_entry = instance.ab_breakpoints_id.first()
    is_disk = breakpoint_entry.Disk_Abx if breakpoint_entry else False

    # Update ab_Disk_RIS
    print(f"{instance.ab_Antibiotic}: MIC={instance.ab_MIC_value}, Disk={instance.ab_Disk_value}, Retest={instance.ab_Retest_DiskValue},Retest={instance.ab_Retest_MICValue},"
      f"R={instance.ab_R_breakpoint}, I={instance.ab_I_breakpoint}, S={instance.ab_S_breakpoint}, SDD={instance.ab_SDD_breakpoint}")
    
    disk_ris = determine_ris(instance.ab_Disk_value, instance.ab_R_breakpoint, instance.ab_I_breakpoint, instance.ab_S_breakpoint, instance.ab_SDD_breakpoint, is_disk=is_disk)
    if disk_ris and disk_ris != instance.ab_Disk_RIS:
        instance.ab_Disk_RIS = disk_ris
        updated_fields.append("ab_Disk_RIS")
    

    # Update ab_MIC_RIS
    mic_ris = determine_ris(instance.ab_MIC_value, instance.ab_R_breakpoint, instance.ab_I_breakpoint, instance.ab_S_breakpoint, instance.ab_SDD_breakpoint)
    if mic_ris and mic_ris != instance.ab_MIC_RIS:
        instance.ab_MIC_RIS = mic_ris
        updated_fields.append("ab_MIC_RIS")
    


    # Update ab_Retest_Disk_RIS
    retest_disk_ris = determine_ris(instance.ab_Retest_DiskValue, instance.ab_Ret_R_breakpoint, instance.ab_Ret_I_breakpoint, instance.ab_Ret_S_breakpoint, instance.ab_Ret_SDD_breakpoint, is_disk=is_disk)
    if retest_disk_ris and retest_disk_ris != instance.ab_Retest_Disk_RIS:
        instance.ab_Retest_Disk_RIS = retest_disk_ris
        updated_fields.append("ab_Retest_Disk_RIS")

    
    
    # Update ab_Retest_MIC_RIS
    retest_mic_ris = determine_ris(instance.ab_Retest_MICValue, instance.ab_Ret_R_breakpoint, instance.ab_Ret_I_breakpoint, instance.ab_Ret_S_breakpoint, instance.ab_Ret_SDD_breakpoint)
    if retest_mic_ris and retest_mic_ris != instance.ab_Retest_MIC_RIS:
        instance.ab_Retest_MIC_RIS = retest_mic_ris
        updated_fields.append("ab_Retest_MIC_RIS")
    

    # Only save if there are updates
    if updated_fields:
        instance.save(update_fields=updated_fields)





# # ==============================
# # SAFE NUMERIC CONVERSION ------ 
# # ==============================
# def to_number(value, is_disk=False):
#     """
#     Convert value to int (disk) or float (MIC).
#     Returns None if empty or invalid.
#     """
#     if value is None:
#         return None

#     s = str(value).strip()
#     if s == "" or s.lower() == "none":
#         return None

#     try:
#         return int(s) if is_disk else float(s)
#     except (ValueError, TypeError):
#         return None


# # ==============================
# # RIS DETERMINATION LOGIC
# # ==============================
# def determine_ris(value, r_bp, i_bp, s_bp, sdd_bp, is_disk=False):
#     """
#     Safely determine RIS based on value and breakpoints.
#     Works for MIC and Disk, including ranges and missing breakpoints.
#     """
#     value = to_number(value, is_disk)
#     if value is None:
#         return None

#     r = to_number(r_bp, is_disk)
#     s = to_number(s_bp, is_disk)
#     sdd = to_number(sdd_bp, is_disk)

#     # ----- INTERMEDIATE RANGE -----
#     if i_bp:
#         try:
#             i_str = str(i_bp).strip()
#             if "-" in i_str:
#                 lo, hi = i_str.split("-")
#                 lo = to_number(lo, is_disk)
#                 hi = to_number(hi, is_disk)
#                 if lo is not None and hi is not None and lo <= value <= hi:
#                     return "I"
#         except Exception:
#             pass

#     # ----- SDD -----
#     if sdd is not None:
#         if is_disk:
#             if value == sdd:
#                 return "SDD"
#         else:
#             if value >= sdd:
#                 return "SDD"

#     # ----- DISK LOGIC -----
#     if is_disk:
#         if r is not None and value <= r:
#             return "R"
#         if s is not None and value >= s:
#             return "S"
#         if r is not None or s is not None:
#             return "I"

#     # ----- MIC LOGIC -----
#     else:
#         if r is not None and value >= r:
#             return "R"
#         if s is not None and value <= s:
#             return "S"
#         if r is not None or s is not None:
#             return "I"
#     return None


# ==============================
# POST-SAVE SIGNAL
# ==============================
# @receiver(post_save, sender=AntibioticEntry)
# def update_ris_interpretation(sender, instance, **kwargs):
#     updated_fields = []

#     # Get related breakpoint entry (ManyToMany)
#     bp = instance.ab_breakpoints_id.first()
#     is_disk = bool(bp and bp.Disk_Abx)

#     # Debug trace (safe)
#     print(
#         f"{instance.ab_Antibiotic}: "
#         f"MIC={instance.ab_MIC_value}, Disk={instance.ab_Disk_value}, "
#         f"R={instance.ab_R_breakpoint}, I={instance.ab_I_breakpoint}, "
#         f"S={instance.ab_S_breakpoint}, SDD={instance.ab_SDD_breakpoint}"
#     )

#     # ---------- PRIMARY DISK ----------
#     disk_ris = determine_ris(
#         instance.ab_Disk_value,
#         instance.ab_R_breakpoint,
#         instance.ab_I_breakpoint,
#         instance.ab_S_breakpoint,
#         instance.ab_SDD_breakpoint,
#         is_disk=True,
#     )
#     if disk_ris and disk_ris != instance.ab_Disk_RIS:
#         instance.ab_Disk_RIS = disk_ris
#         updated_fields.append("ab_Disk_RIS")

#     # ---------- PRIMARY MIC ----------
#     mic_ris = determine_ris(
#         instance.ab_MIC_value,
#         instance.ab_R_breakpoint,
#         instance.ab_I_breakpoint,
#         instance.ab_S_breakpoint,
#         instance.ab_SDD_breakpoint,
#         is_disk=False,
#     )
#     if mic_ris and mic_ris != instance.ab_MIC_RIS:
#         instance.ab_MIC_RIS = mic_ris
#         updated_fields.append("ab_MIC_RIS")

#     # ---------- RETEST DISK ----------
#     ret_disk_ris = determine_ris(
#         instance.ab_Retest_DiskValue,
#         instance.ab_Ret_R_breakpoint,
#         instance.ab_Ret_I_breakpoint,
#         instance.ab_Ret_S_breakpoint,
#         instance.ab_Ret_SDD_breakpoint,
#         is_disk=True,
#     )
#     if ret_disk_ris and ret_disk_ris != instance.ab_Retest_Disk_RIS:
#         instance.ab_Retest_Disk_RIS = ret_disk_ris
#         updated_fields.append("ab_Retest_Disk_RIS")

#     # ---------- RETEST MIC ----------
#     ret_mic_ris = determine_ris(
#         instance.ab_Retest_MICValue,
#         instance.ab_Ret_R_breakpoint,
#         instance.ab_Ret_I_breakpoint,
#         instance.ab_Ret_S_breakpoint,
#         instance.ab_Ret_SDD_breakpoint,
#         is_disk=False,
#     )
#     if ret_mic_ris and ret_mic_ris != instance.ab_Retest_MIC_RIS:
#         instance.ab_Retest_MIC_RIS = ret_mic_ris
#         updated_fields.append("ab_Retest_MIC_RIS")

#     # ---------- SAVE ONLY IF NEEDED ----------
#     if updated_fields:
#         instance.save(update_fields=updated_fields)



# from django.db.models.signals import m2m_changed
# from django.dispatch import receiver

# @receiver(m2m_changed, sender=AntibioticEntry.ab_breakpoints_id.through)
# def update_ris_after_breakpoint_set(sender, instance, action, **kwargs):
#     if action not in ("post_add", "post_remove", "post_clear"):
#         return

#     updated_fields = []

#     bp = instance.ab_breakpoints_id.first()
#     if not bp:
#         return

#     is_disk = bool(bp.Disk_Abx)

#     # ---------- DISK ----------
#     disk_ris = determine_ris(
#         instance.ab_Disk_value,
#         instance.ab_R_breakpoint,
#         instance.ab_I_breakpoint,
#         instance.ab_S_breakpoint,
#         instance.ab_SDD_breakpoint,
#         is_disk=True,
#     )
#     if disk_ris and disk_ris != instance.ab_Disk_RIS:
#         instance.ab_Disk_RIS = disk_ris
#         updated_fields.append("ab_Disk_RIS")

#     # ---------- MIC ----------
#     mic_ris = determine_ris(
#         instance.ab_MIC_value,
#         instance.ab_R_breakpoint,
#         instance.ab_I_breakpoint,
#         instance.ab_S_breakpoint,
#         instance.ab_SDD_breakpoint,
#         is_disk=False,
#     )
#     if mic_ris and mic_ris != instance.ab_MIC_RIS:
#         instance.ab_MIC_RIS = mic_ris
#         updated_fields.append("ab_MIC_RIS")

#     # ---------- RETEST DISK ----------
#     ret_disk_ris = determine_ris(
#         instance.ab_Retest_DiskValue,
#         instance.ab_Ret_R_breakpoint,
#         instance.ab_Ret_I_breakpoint,
#         instance.ab_Ret_S_breakpoint,
#         instance.ab_Ret_SDD_breakpoint,
#         is_disk=True,
#     )
#     if ret_disk_ris and ret_disk_ris != instance.ab_Retest_Disk_RIS:
#         instance.ab_Retest_Disk_RIS = ret_disk_ris
#         updated_fields.append("ab_Retest_Disk_RIS")

#     # ---------- RETEST MIC ----------
#     ret_mic_ris = determine_ris(
#         instance.ab_Retest_MICValue,
#         instance.ab_Ret_R_breakpoint,
#         instance.ab_Ret_I_breakpoint,
#         instance.ab_Ret_S_breakpoint,
#         instance.ab_Ret_SDD_breakpoint,
#         is_disk=False,
#     )
#     if ret_mic_ris and ret_mic_ris != instance.ab_Retest_MIC_RIS:
#         instance.ab_Retest_MIC_RIS = ret_mic_ris
#         updated_fields.append("ab_Retest_MIC_RIS")

#     if updated_fields:
#         instance.save(update_fields=updated_fields)