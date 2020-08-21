# uncompyle6 version 3.6.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.17 (default, Jul 20 2020, 15:37:01) 
# [GCC 7.5.0]
# Embedded file name: /Applications/Ableton Live 9 Suite.app/Contents/App-Resources/MIDI Remote Scripts/Hercules_P32_DJ/hercules_p32_dj.py
# Compiled at: 2017-10-20 11:12:58
from __future__ import with_statement
import Live
from _Framework.ControlSurface import ControlSurface
from _Framework.DeviceComponent import DeviceComponent
from _Framework.MixerComponent import MixerComponent
from _Framework.SliderElement import SliderElement
from _Framework.TransportComponent import TransportComponent
from _Framework.InputControlElement import *
from _Framework.ButtonElement import ButtonElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.SessionComponent import SessionComponent
from _Framework.EncoderElement import *
from Launchpad.ConfigurableButtonElement import ConfigurableButtonElement

class hercules_p32_dj(ControlSurface):

    def __init__(self, c_instance):
        global _map_modes
        global active_mode
        super(hercules_p32_dj, self).__init__(c_instance)
        with self.component_guard():
            _map_modes = Live.MidiMap.MapMode
            self.current_track_offset = 0
            self.current_scene_offset = 0
            num_tracks = 128
            num_returns = 24
            self.mixer = MixerComponent(num_tracks, num_returns)
            self._mode0()
            active_mode = '_mode1'
            self._set_active_mode()
            self._set_track_select_led()
            self.show_message('Powered by remotify.io')

    def _mode2(self):
        self.show_message('_mode2 is active')
        num_tracks = 4
        num_scenes = 4
        self._session = SessionComponent(num_tracks, num_scenes)
        track_offset = self.current_track_offset
        scene_offset = self.current_scene_offset
        self._session.set_offsets(track_offset, scene_offset)
        self._session._reassign_scenes()
        self.set_highlighting_session_component(self._session)
        session_buttons = [
         48, 49, 50, 51, 44, 45, 46, 47, 40, 41, 42, 43, 36, 37, 38, 39]
        session_channels = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        session_types = [MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE]
        session_is_momentary = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        self._pads = [ ButtonElement(session_is_momentary[index], session_types[index], session_channels[index], session_buttons[index]) for index in range(num_tracks * num_scenes) ]
        self._grid = ButtonMatrixElement(rows=[ self._pads[index * num_tracks:index * num_tracks + num_tracks] for index in range(num_scenes) ])
        self._session.set_clip_launch_buttons(self._grid)
        stop_all_button = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 2, 6)
        self._session.set_stop_all_clips_button(stop_all_button)
        stop_track_buttons = [
         3, 4, 5, 6]
        stop_track_channels = [1, 1, 1, 1]
        stop_track_types = [MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE]
        stop_track_is_momentary = [1, 1, 1, 1]
        self._track_stop_buttons = [ ConfigurableButtonElement(stop_track_is_momentary[index], stop_track_types[index], stop_track_channels[index], stop_track_buttons[index]) for index in range(num_tracks) ]
        self._session.set_stop_track_clip_buttons(tuple(self._track_stop_buttons))
        self._session._enable_skinning()
        self._session.set_stop_clip_triggered_value(127)
        self._session.set_stop_clip_value(81)
        for scene_index in range(num_scenes):
            scene = self._session.scene(scene_index)
            scene.set_scene_value(81)
            scene.set_no_scene_value(0)
            scene.set_triggered_value(127)
            for track_index in range(num_tracks):
                clip_slot = scene.clip_slot(track_index)
                clip_slot.set_triggered_to_play_value(41)
                clip_slot.set_triggered_to_record_value(30)
                clip_slot.set_record_button_value(10)
                clip_slot.set_stopped_value(81)
                clip_slot.set_started_value(126)
                clip_slot.set_recording_value(125)

        for index in range(num_tracks):
            stop_track_button = self._session._stop_track_clip_buttons[index]
            stop_track_button.set_on_off_values(81, 0)

        stop_all_button.set_on_off_values(127, 0)
        self.session_right = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 5, 42)
        self._session.set_track_bank_right_button(self.session_right)
        self.session_right.add_value_listener(self._reload_active_devices, identify_sender=False)
        self.session_left = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 5, 40)
        self._session.set_track_bank_left_button(self.session_left)
        self.session_left.add_value_listener(self._reload_active_devices, identify_sender=False)
        self.session_down = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 5, 37)
        self._session.set_scene_bank_down_button(self.session_down)
        self.session_down.add_value_listener(self._reload_active_devices, identify_sender=False)
        self.session_up = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 5, 45)
        self._session.set_scene_bank_up_button(self.session_up)
        self.session_up.add_value_listener(self._reload_active_devices, identify_sender=False)
        self.refresh_state()
        self._mode2_devices()
        self.add_device_listeners()
        self.mode_2_to_1 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 0, 1)
        self.mode_2_to_1.add_value_listener(self._activate_mode1, identify_sender=False)

    def _remove_mode2(self):
        self._remove_mode2_devices()
        self.remove_device_listeners()
        self._session.set_clip_launch_buttons(None)
        self.set_highlighting_session_component(None)
        self._session.set_stop_all_clips_button(None)
        self._track_stop_buttons = None
        self._session.set_stop_track_clip_buttons(None)
        self.session_right.remove_value_listener(self._reload_active_devices)
        self._session.set_track_bank_right_button(None)
        self.session_left.remove_value_listener(self._reload_active_devices)
        self._session.set_track_bank_left_button(None)
        self.session_down.remove_value_listener(self._reload_active_devices)
        self._session.set_scene_bank_down_button(None)
        self.session_up.remove_value_listener(self._reload_active_devices)
        self._session.set_scene_bank_up_button(None)
        self.current_track_offset = self._session._track_offset
        self.current_scene_offset = self._session._scene_offset
        self._session = None
        self.mode_2_to_1.remove_value_listener(self._activate_mode1)
        self.mode_2_to_1 = None
        return

    def _mode2_devices(self):
        if len(self.mixer.selected_strip()._track.devices) > 0:
            self.device_tracktype_selected__chain_number_selected = DeviceComponent()
            device_controls = (
             EncoderElement(MIDI_CC_TYPE, 1, 4, _map_modes.absolute),
             EncoderElement(MIDI_CC_TYPE, 1, 3, _map_modes.absolute),
             EncoderElement(MIDI_CC_TYPE, 1, 2, _map_modes.absolute),
             EncoderElement(MIDI_CC_TYPE, 1, 1, _map_modes.absolute),
             EncoderElement(MIDI_CC_TYPE, 2, 4, _map_modes.absolute),
             EncoderElement(MIDI_CC_TYPE, 2, 3, _map_modes.absolute),
             EncoderElement(MIDI_CC_TYPE, 2, 2, _map_modes.absolute),
             EncoderElement(MIDI_CC_TYPE, 2, 1, _map_modes.absolute))
            self.device_tracktype_selected__chain_number_selected.set_parameter_controls(tuple(device_controls))
            self.set_device_component(self.device_tracktype_selected__chain_number_selected)

    def _remove_mode2_devices(self):
        if hasattr(self, 'device_tracktype_selected__chain_number_selected'):
            device_controls = (None, None, None, None, None, None, None, None)
            self.device_tracktype_selected__chain_number_selected.set_parameter_controls(tuple(device_controls))
            self.set_device_component(self.device_tracktype_selected__chain_number_selected)
        return

    def _mode1(self):
        self.show_message('_mode1 is active')
        num_tracks = 7
        num_scenes = 4
        self._session = SessionComponent(num_tracks, num_scenes)
        track_offset = self.current_track_offset
        scene_offset = self.current_scene_offset
        self._session.set_offsets(track_offset, scene_offset)
        self._session._reassign_scenes()
        self.set_highlighting_session_component(self._session)
        session_buttons = [
         48, 49, 50, 51, 48, 49, 50, 44, 45, 46, 47, 44, 45, 46, 40, 41, 42, 43, 40, 41, 42, 36, 37, 38, 39, 36, 37, 38]
        session_channels = [1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2]
        session_types = [MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE]
        session_is_momentary = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        self._pads = [ ButtonElement(session_is_momentary[index], session_types[index], session_channels[index], session_buttons[index]) for index in range(num_tracks * num_scenes) ]
        self._grid = ButtonMatrixElement(rows=[ self._pads[index * num_tracks:index * num_tracks + num_tracks] for index in range(num_scenes) ])
        self._session.set_clip_launch_buttons(self._grid)
        stop_all_button = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 2, 6)
        self._session.set_stop_all_clips_button(stop_all_button)
        stop_track_buttons = [
         3, 4, 5, 6, 3, 4, 5]
        stop_track_channels = [1, 1, 1, 1, 2, 2, 2]
        stop_track_types = [MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE]
        stop_track_is_momentary = [1, 1, 1, 1, 1, 1, 1]
        self._track_stop_buttons = [ ConfigurableButtonElement(stop_track_is_momentary[index], stop_track_types[index], stop_track_channels[index], stop_track_buttons[index]) for index in range(num_tracks) ]
        self._session.set_stop_track_clip_buttons(tuple(self._track_stop_buttons))
        scene_buttons = [
         51, 47, 43, 39]
        scene_channels = [2, 2, 2, 2]
        scene_types = [MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE, MIDI_NOTE_TYPE]
        scene_momentarys = [1, 1, 1, 1]
        self._scene_launch_buttons = [ ButtonElement(scene_momentarys[index], scene_types[index], scene_channels[index], scene_buttons[index]) for index in range(num_scenes) ]
        self._scene_launch_buttons = ButtonMatrixElement(rows=[self._scene_launch_buttons])
        self._session.set_scene_launch_buttons(self._scene_launch_buttons)
        self._session._enable_skinning()
        self._session.set_stop_clip_triggered_value(127)
        self._session.set_stop_clip_value(81)
        for scene_index in range(num_scenes):
            scene = self._session.scene(scene_index)
            scene.set_scene_value(81)
            scene.set_no_scene_value(0)
            scene.set_triggered_value(127)
            for track_index in range(num_tracks):
                clip_slot = scene.clip_slot(track_index)
                clip_slot.set_triggered_to_play_value(41)
                clip_slot.set_triggered_to_record_value(30)
                clip_slot.set_record_button_value(10)
                clip_slot.set_stopped_value(81)
                clip_slot.set_started_value(126)
                clip_slot.set_recording_value(125)

        for index in range(num_tracks):
            stop_track_button = self._session._stop_track_clip_buttons[index]
            stop_track_button.set_on_off_values(81, 0)

        stop_all_button.set_on_off_values(127, 0)
        self.session_up = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 5, 45)
        self._session.set_scene_bank_up_button(self.session_up)
        self.session_up.add_value_listener(self._reload_active_devices, identify_sender=False)
        self.session_left = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 5, 40)
        self._session.set_track_bank_left_button(self.session_left)
        self.session_left.add_value_listener(self._reload_active_devices, identify_sender=False)
        self.session_right = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 5, 42)
        self._session.set_track_bank_right_button(self.session_right)
        self.session_right.add_value_listener(self._reload_active_devices, identify_sender=False)
        self.session_down = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 5, 37)
        self._session.set_scene_bank_down_button(self.session_down)
        self.session_down.add_value_listener(self._reload_active_devices, identify_sender=False)
        self._session._link()
        self.refresh_state()
        self._mode1_devices()
        self.add_device_listeners()
        self.mode_1_to_2 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 0, 1)
        self.mode_1_to_2.add_value_listener(self._activate_mode2, identify_sender=False)

    def _remove_mode1(self):
        self._remove_mode1_devices()
        self.remove_device_listeners()
        self._session.set_clip_launch_buttons(None)
        self.set_highlighting_session_component(None)
        self._session.set_stop_all_clips_button(None)
        self._track_stop_buttons = None
        self._session.set_stop_track_clip_buttons(None)
        self._scene_launch_buttons = None
        self._session.set_scene_launch_buttons(None)
        self.session_up.remove_value_listener(self._reload_active_devices)
        self._session.set_scene_bank_up_button(None)
        self.session_left.remove_value_listener(self._reload_active_devices)
        self._session.set_track_bank_left_button(None)
        self.session_right.remove_value_listener(self._reload_active_devices)
        self._session.set_track_bank_right_button(None)
        self.session_down.remove_value_listener(self._reload_active_devices)
        self._session.set_scene_bank_down_button(None)
        self.current_track_offset = self._session._track_offset
        self.current_scene_offset = self._session._scene_offset
        self._session._unlink()
        self._session = None
        self.mode_1_to_2.remove_value_listener(self._activate_mode2)
        self.mode_1_to_2 = None
        return

    def _mode1_devices(self):
        device_number = 0
        if len(self.mixer.selected_strip()._track.devices) > device_number:
            devices = self.mixer.selected_strip()._track.devices
            self.actual_device = devices[device_number]
            self.device_tracktype_selected__chain_number_1 = DeviceComponent()
            device_controls = (
             EncoderElement(MIDI_CC_TYPE, 1, 4, _map_modes.absolute),
             EncoderElement(MIDI_CC_TYPE, 1, 3, _map_modes.absolute),
             EncoderElement(MIDI_CC_TYPE, 1, 2, _map_modes.absolute),
             EncoderElement(MIDI_CC_TYPE, 1, 1, _map_modes.absolute),
             EncoderElement(MIDI_CC_TYPE, 2, 4, _map_modes.absolute),
             EncoderElement(MIDI_CC_TYPE, 2, 3, _map_modes.absolute),
             EncoderElement(MIDI_CC_TYPE, 2, 2, _map_modes.absolute),
             EncoderElement(MIDI_CC_TYPE, 2, 1, _map_modes.absolute))
            self.device_tracktype_selected__chain_number_1.set_device(self.actual_device)
            self.device_tracktype_selected__chain_number_1.set_parameter_controls(tuple(device_controls))
            self.device_tracktype_selected__chain_number_1.set_lock_to_device('lock', self.actual_device)

    def _remove_mode1_devices(self):
        device_number = 0
        if hasattr(self, 'device_tracktype_selected__chain_number_1'):
            device_controls = (None, None, None, None, None, None, None, None)
            self.device_tracktype_selected__chain_number_1.set_parameter_controls(tuple(device_controls))
            self.device_tracktype_selected__chain_number_1.set_lock_to_device('', self.actual_device)
            self.device_tracktype_selected__chain_number_1.set_device(None)
        return

    def _mode0(self):
        global direction_tempo_control_updown_mode0
        global direction_tempo_fine_control_updown_mode0
        global lv_tempo_control_updown_mode0
        global lv_tempo_fine_control_updown_mode0
        self.show_message('_mode0 is active')
        self.mixer.set_crossfader_control(EncoderElement(MIDI_CC_TYPE, 0, 1, _map_modes.absolute))
        self.mixer.channel_strip(0).set_volume_control(EncoderElement(MIDI_CC_TYPE, 1, 6, _map_modes.absolute))
        self.mixer.channel_strip(1).set_volume_control(EncoderElement(MIDI_CC_TYPE, 1, 7, _map_modes.absolute))
        self.mixer.channel_strip(2).set_volume_control(EncoderElement(MIDI_CC_TYPE, 1, 8, _map_modes.absolute))
        self.mixer.channel_strip(3).set_volume_control(EncoderElement(MIDI_CC_TYPE, 1, 9, _map_modes.absolute))
        self.mixer.channel_strip(4).set_volume_control(EncoderElement(MIDI_CC_TYPE, 2, 6, _map_modes.absolute))
        self.mixer.channel_strip(5).set_volume_control(EncoderElement(MIDI_CC_TYPE, 2, 7, _map_modes.absolute))
        self.mixer.channel_strip(6).set_volume_control(EncoderElement(MIDI_CC_TYPE, 2, 8, _map_modes.absolute))
        self.mixer.master_strip().set_volume_control(EncoderElement(MIDI_CC_TYPE, 2, 9, _map_modes.absolute))
        arm_specific_0 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 1, 52)
        arm_specific_0.set_on_off_values(125, 1)
        self.mixer.channel_strip(0).set_arm_button(arm_specific_0)
        arm_specific_1 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 1, 53)
        arm_specific_1.set_on_off_values(125, 1)
        self.mixer.channel_strip(1).set_arm_button(arm_specific_1)
        arm_specific_2 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 1, 54)
        arm_specific_2.set_on_off_values(125, 1)
        self.mixer.channel_strip(2).set_arm_button(arm_specific_2)
        arm_specific_3 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 1, 55)
        arm_specific_3.set_on_off_values(125, 1)
        self.mixer.channel_strip(3).set_arm_button(arm_specific_3)
        arm_specific_4 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 2, 52)
        arm_specific_4.set_on_off_values(125, 1)
        self.mixer.channel_strip(4).set_arm_button(arm_specific_4)
        arm_specific_5 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 2, 53)
        arm_specific_5.set_on_off_values(125, 1)
        self.mixer.channel_strip(5).set_arm_button(arm_specific_5)
        arm_specific_6 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 2, 54)
        arm_specific_6.set_on_off_values(125, 1)
        self.mixer.channel_strip(6).set_arm_button(arm_specific_6)
        solo_specific_0 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 1, 56)
        solo_specific_0.set_on_off_values(126, 41)
        self.mixer.channel_strip(0).set_solo_button(solo_specific_0)
        solo_specific_1 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 1, 57)
        solo_specific_1.set_on_off_values(126, 41)
        self.mixer.channel_strip(1).set_solo_button(solo_specific_1)
        solo_specific_2 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 1, 58)
        solo_specific_2.set_on_off_values(126, 41)
        self.mixer.channel_strip(2).set_solo_button(solo_specific_2)
        solo_specific_3 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 1, 59)
        solo_specific_3.set_on_off_values(126, 41)
        self.mixer.channel_strip(3).set_solo_button(solo_specific_3)
        solo_specific_4 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 2, 56)
        solo_specific_4.set_on_off_values(126, 41)
        self.mixer.channel_strip(4).set_solo_button(solo_specific_4)
        solo_specific_5 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 2, 57)
        solo_specific_5.set_on_off_values(126, 41)
        self.mixer.channel_strip(5).set_solo_button(solo_specific_5)
        solo_specific_6 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 2, 58)
        solo_specific_6.set_on_off_values(126, 41)
        self.mixer.channel_strip(6).set_solo_button(solo_specific_6)
        mute_specific_0 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 1, 60)
        mute_specific_0.set_on_off_values(127, 81)
        self.mixer.channel_strip(0).set_mute_button(mute_specific_0)
        self.mixer.channel_strip(0).set_invert_mute_feedback(True)
        mute_specific_1 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 1, 61)
        mute_specific_1.set_on_off_values(127, 81)
        self.mixer.channel_strip(1).set_mute_button(mute_specific_1)
        self.mixer.channel_strip(1).set_invert_mute_feedback(True)
        mute_specific_2 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 1, 62)
        mute_specific_2.set_on_off_values(127, 81)
        self.mixer.channel_strip(2).set_mute_button(mute_specific_2)
        self.mixer.channel_strip(2).set_invert_mute_feedback(True)
        mute_specific_3 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 1, 63)
        mute_specific_3.set_on_off_values(127, 81)
        self.mixer.channel_strip(3).set_mute_button(mute_specific_3)
        self.mixer.channel_strip(3).set_invert_mute_feedback(True)
        mute_specific_4 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 2, 60)
        mute_specific_4.set_on_off_values(127, 81)
        self.mixer.channel_strip(4).set_mute_button(mute_specific_4)
        self.mixer.channel_strip(4).set_invert_mute_feedback(True)
        mute_specific_5 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 2, 61)
        mute_specific_5.set_on_off_values(127, 81)
        self.mixer.channel_strip(5).set_mute_button(mute_specific_5)
        self.mixer.channel_strip(5).set_invert_mute_feedback(True)
        mute_specific_6 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 2, 62)
        mute_specific_6.set_on_off_values(127, 81)
        self.mixer.channel_strip(6).set_mute_button(mute_specific_6)
        self.mixer.channel_strip(6).set_invert_mute_feedback(True)
        self.trackselect7 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 2, 66)
        self.trackselect7.set_on_off_values(127, 81)
        self.trackselect7.add_value_listener(self.track_select_7, identify_sender=False)
        self.trackselect6 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 2, 65)
        self.trackselect6.set_on_off_values(127, 81)
        self.trackselect6.add_value_listener(self.track_select_6, identify_sender=False)
        self.trackselect5 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 2, 64)
        self.trackselect5.set_on_off_values(127, 81)
        self.trackselect5.add_value_listener(self.track_select_5, identify_sender=False)
        self.trackselect4 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 1, 67)
        self.trackselect4.set_on_off_values(127, 81)
        self.trackselect4.add_value_listener(self.track_select_4, identify_sender=False)
        self.trackselect3 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 1, 66)
        self.trackselect3.set_on_off_values(127, 81)
        self.trackselect3.add_value_listener(self.track_select_3, identify_sender=False)
        self.trackselect2 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 1, 65)
        self.trackselect2.set_on_off_values(127, 81)
        self.trackselect2.add_value_listener(self.track_select_2, identify_sender=False)
        self.trackselect1 = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 1, 64)
        self.trackselect1.set_on_off_values(127, 81)
        self.trackselect1.add_value_listener(self.track_select_1, identify_sender=False)
        self.transport = TransportComponent()
        self.transport.name = 'Transport'
        lv_tempo_fine_control_updown_mode0 = 0
        direction_tempo_fine_control_updown_mode0 = 'not set'
        self.tempo_fine_control_updown_encoder = EncoderElement(MIDI_CC_TYPE, 4, 10, _map_modes.relative_smooth_two_compliment)
        self.tempo_fine_control_updown_encoder.add_value_listener(self.tempo_fine_control_updown_mode0, identify_sender=False)
        lv_tempo_control_updown_mode0 = 0
        direction_tempo_control_updown_mode0 = 'not set'
        self.tempo_control_updown_encoder = EncoderElement(MIDI_CC_TYPE, 1, 10, _map_modes.relative_smooth_two_compliment)
        self.tempo_control_updown_encoder.add_value_listener(self.tempo_control_updown_mode0, identify_sender=False)
        metronome_button = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 1, 1)
        metronome_button.name = 'metronome_button'
        self.transport.set_metronome_button(metronome_button)
        play_button = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 2, 10)
        play_button.set_on_off_values(127, 0)
        play_button.name = 'play_button'
        self.transport.set_play_button(play_button)
        stop_button = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 2, 9)
        stop_button.set_on_off_values(127, 0)
        stop_button.name = 'stop_button'
        self.transport.set_stop_button(stop_button)
        record_button = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 0, 2)
        record_button.set_on_off_values(127, 0)
        record_button.name = 'record_button'
        self.transport.set_record_button(record_button)
        overdub_button = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 0, 3)
        overdub_button.set_on_off_values(127, 0)
        overdub_button.name = 'overdub_button'
        self.transport.set_overdub_button(overdub_button)
        self.trackleft = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 1, 15)
        self.trackleft.add_value_listener(self._trackleft_track_nav, identify_sender=False)
        self.trackright = ConfigurableButtonElement(1, MIDI_NOTE_TYPE, 2, 15)
        self.trackright.add_value_listener(self._trackright_track_nav, identify_sender=False)

    def _remove_mode0(self):
        self.mixer.set_crossfader_control(None)
        self.mixer.channel_strip(0).set_volume_control(None)
        self.mixer.channel_strip(1).set_volume_control(None)
        self.mixer.channel_strip(2).set_volume_control(None)
        self.mixer.channel_strip(3).set_volume_control(None)
        self.mixer.channel_strip(4).set_volume_control(None)
        self.mixer.channel_strip(5).set_volume_control(None)
        self.mixer.channel_strip(6).set_volume_control(None)
        self.mixer.master_strip().set_volume_control(None)
        self.mixer.channel_strip(0).set_arm_button(None)
        self.mixer.channel_strip(1).set_arm_button(None)
        self.mixer.channel_strip(2).set_arm_button(None)
        self.mixer.channel_strip(3).set_arm_button(None)
        self.mixer.channel_strip(4).set_arm_button(None)
        self.mixer.channel_strip(5).set_arm_button(None)
        self.mixer.channel_strip(6).set_arm_button(None)
        self.mixer.channel_strip(0).set_solo_button(None)
        self.mixer.channel_strip(1).set_solo_button(None)
        self.mixer.channel_strip(2).set_solo_button(None)
        self.mixer.channel_strip(3).set_solo_button(None)
        self.mixer.channel_strip(4).set_solo_button(None)
        self.mixer.channel_strip(5).set_solo_button(None)
        self.mixer.channel_strip(6).set_solo_button(None)
        self.mixer.channel_strip(0).set_mute_button(None)
        self.mixer.channel_strip(1).set_mute_button(None)
        self.mixer.channel_strip(2).set_mute_button(None)
        self.mixer.channel_strip(3).set_mute_button(None)
        self.mixer.channel_strip(4).set_mute_button(None)
        self.mixer.channel_strip(5).set_mute_button(None)
        self.mixer.channel_strip(6).set_mute_button(None)
        self.trackselect7.send_value(0)
        self.trackselect7.remove_value_listener(self.track_select_7)
        self.trackselect7 = None
        self.trackselect6.send_value(0)
        self.trackselect6.remove_value_listener(self.track_select_6)
        self.trackselect6 = None
        self.trackselect5.send_value(0)
        self.trackselect5.remove_value_listener(self.track_select_5)
        self.trackselect5 = None
        self.trackselect4.send_value(0)
        self.trackselect4.remove_value_listener(self.track_select_4)
        self.trackselect4 = None
        self.trackselect3.send_value(0)
        self.trackselect3.remove_value_listener(self.track_select_3)
        self.trackselect3 = None
        self.trackselect2.send_value(0)
        self.trackselect2.remove_value_listener(self.track_select_2)
        self.trackselect2 = None
        self.trackselect1.send_value(0)
        self.trackselect1.remove_value_listener(self.track_select_1)
        self.trackselect1 = None
        self.tempo_fine_control_updown_encoder.remove_value_listener(self.tempo_fine_control_updown_mode0)
        self.tempo_fine_control_updown_encoder = None
        self.tempo_control_updown_encoder.remove_value_listener(self.tempo_control_updown_mode0)
        self.tempo_control_updown_encoder = None
        self.transport.set_tempo_fine_control(None)
        self.transport.set_tempo_control(None)
        self.transport.set_metronome_button(None)
        self.transport.set_play_button(None)
        self.transport.set_stop_button(None)
        self.transport.set_record_button(None)
        self.transport.set_overdub_button(None)
        self.transport = None
        self.trackleft.remove_value_listener(self._trackleft_track_nav)
        self.trackleft = None
        self.trackright.remove_value_listener(self._trackright_track_nav)
        self.trackright = None
        return

    def add_device_listeners(self):
        num_of_tracks = len(self.song().tracks)
        value = 'add device listener'
        for index in range(num_of_tracks):
            self.song().tracks[index].view.add_selected_device_listener(self._reload_active_devices)

    def remove_device_listeners(self):
        num_of_tracks = len(self.song().tracks)
        value = 'remove device listener'
        for index in range(num_of_tracks):
            if hasattr(self.song().tracks[index].view, 'remove_selected_device_listener'):
                self.song().tracks[index].view.remove_selected_device_listener(self._reload_active_devices)

    def _reload_active_devices(self, value=None):
        self._remove_active_devices()
        self._set_active_devices()
        if hasattr(self, '_turn_on_device_select_leds'):
            self._turn_off_device_select_leds()
            self._turn_on_device_select_leds()
        if hasattr(self, '_all_prev_device_leds'):
            self._all_prev_device_leds()
        if hasattr(self, '_all_nxt_device_leds'):
            self._all_nxt_device_leds()

    def _set_active_devices(self):
        if active_mode == '_mode2' and hasattr(self, '_mode2_devices'):
            self._mode2_devices()
        else:
            if active_mode == '_mode1' and hasattr(self, '_mode1_devices'):
                self._mode1_devices()
            else:
                if active_mode == '_mode0' and hasattr(self, '_mode0_devices'):
                    self._mode0_devices()

    def _remove_active_devices(self):
        if active_mode == '_mode2' and hasattr(self, '_mode2_devices'):
            self._remove_mode2_devices()
        else:
            if active_mode == '_mode1' and hasattr(self, '_mode1_devices'):
                self._remove_mode1_devices()
            else:
                if active_mode == '_mode0' and hasattr(self, '_mode0_devices'):
                    self._remove_mode0_devices()

    def _set_track_select_led(self):
        self._turn_off_track_select_leds()
        offset = 0
        if hasattr(self, '_session'):
            offset = self._session._track_offset
        num_of_tracks = len(self.song().tracks)
        pos = offset + 6
        pos2 = pos + 1
        if num_of_tracks >= pos2:
            if self.song().view.selected_track == self.song().tracks[pos]:
                if hasattr(self, 'trackselect7') and self.trackselect7 is not None:
                    self.trackselect7.send_value(127)
        pos = offset + 5
        pos2 = pos + 1
        if num_of_tracks >= pos2:
            if self.song().view.selected_track == self.song().tracks[pos]:
                if hasattr(self, 'trackselect6') and self.trackselect6 is not None:
                    self.trackselect6.send_value(127)
        pos = offset + 4
        pos2 = pos + 1
        if num_of_tracks >= pos2:
            if self.song().view.selected_track == self.song().tracks[pos]:
                if hasattr(self, 'trackselect5') and self.trackselect5 is not None:
                    self.trackselect5.send_value(127)
        pos = offset + 3
        pos2 = pos + 1
        if num_of_tracks >= pos2:
            if self.song().view.selected_track == self.song().tracks[pos]:
                if hasattr(self, 'trackselect4') and self.trackselect4 is not None:
                    self.trackselect4.send_value(127)
        pos = offset + 2
        pos2 = pos + 1
        if num_of_tracks >= pos2:
            if self.song().view.selected_track == self.song().tracks[pos]:
                if hasattr(self, 'trackselect3') and self.trackselect3 is not None:
                    self.trackselect3.send_value(127)
        pos = offset + 1
        pos2 = pos + 1
        if num_of_tracks >= pos2:
            if self.song().view.selected_track == self.song().tracks[pos]:
                if hasattr(self, 'trackselect2') and self.trackselect2 is not None:
                    self.trackselect2.send_value(127)
        pos = offset + 0
        pos2 = pos + 1
        if num_of_tracks >= pos2:
            if self.song().view.selected_track == self.song().tracks[pos]:
                if hasattr(self, 'trackselect1') and self.trackselect1 is not None:
                    self.trackselect1.send_value(127)
        return

    def _turn_off_track_select_leds(self):
        num_of_tracks = len(self.song().tracks)
        offset = 0
        if hasattr(self, '_session'):
            offset = self._session._track_offset
        pos = offset + 6
        pos2 = pos + 1
        if num_of_tracks >= pos2 and hasattr(self, 'trackselect7') and self.trackselect7 is not None:
            self.trackselect7.send_value(81)
        else:
            if num_of_tracks < pos2 and hasattr(self, 'trackselect7') and self.trackselect7 is not None:
                self.trackselect7.send_value(0)
        pos = offset + 5
        pos2 = pos + 1
        if num_of_tracks >= pos2 and hasattr(self, 'trackselect6') and self.trackselect6 is not None:
            self.trackselect6.send_value(81)
        else:
            if num_of_tracks < pos2 and hasattr(self, 'trackselect6') and self.trackselect6 is not None:
                self.trackselect6.send_value(0)
        pos = offset + 4
        pos2 = pos + 1
        if num_of_tracks >= pos2 and hasattr(self, 'trackselect5') and self.trackselect5 is not None:
            self.trackselect5.send_value(81)
        else:
            if num_of_tracks < pos2 and hasattr(self, 'trackselect5') and self.trackselect5 is not None:
                self.trackselect5.send_value(0)
        pos = offset + 3
        pos2 = pos + 1
        if num_of_tracks >= pos2 and hasattr(self, 'trackselect4') and self.trackselect4 is not None:
            self.trackselect4.send_value(81)
        else:
            if num_of_tracks < pos2 and hasattr(self, 'trackselect4') and self.trackselect4 is not None:
                self.trackselect4.send_value(0)
        pos = offset + 2
        pos2 = pos + 1
        if num_of_tracks >= pos2 and hasattr(self, 'trackselect3') and self.trackselect3 is not None:
            self.trackselect3.send_value(81)
        else:
            if num_of_tracks < pos2 and hasattr(self, 'trackselect3') and self.trackselect3 is not None:
                self.trackselect3.send_value(0)
        pos = offset + 1
        pos2 = pos + 1
        if num_of_tracks >= pos2 and hasattr(self, 'trackselect2') and self.trackselect2 is not None:
            self.trackselect2.send_value(81)
        else:
            if num_of_tracks < pos2 and hasattr(self, 'trackselect2') and self.trackselect2 is not None:
                self.trackselect2.send_value(0)
        pos = offset + 0
        pos2 = pos + 1
        if num_of_tracks >= pos2 and hasattr(self, 'trackselect1') and self.trackselect1 is not None:
            self.trackselect1.send_value(81)
        else:
            if num_of_tracks < pos2 and hasattr(self, 'trackselect1') and self.trackselect1 is not None:
                self.trackselect1.send_value(0)
        return

    def track_select_7(self, value):
        if value > 0:
            if hasattr(self, '_session'):
                move = self._session._track_offset + 7
            else:
                move = 7
            num_of_tracks = len(self.song().tracks)
            if num_of_tracks >= move:
                move = move - 1
                self.song().view.selected_track = self.song().tracks[move]

    def track_select_6(self, value):
        if value > 0:
            if hasattr(self, '_session'):
                move = self._session._track_offset + 6
            else:
                move = 6
            num_of_tracks = len(self.song().tracks)
            if num_of_tracks >= move:
                move = move - 1
                self.song().view.selected_track = self.song().tracks[move]

    def track_select_5(self, value):
        if value > 0:
            if hasattr(self, '_session'):
                move = self._session._track_offset + 5
            else:
                move = 5
            num_of_tracks = len(self.song().tracks)
            if num_of_tracks >= move:
                move = move - 1
                self.song().view.selected_track = self.song().tracks[move]

    def track_select_4(self, value):
        if value > 0:
            if hasattr(self, '_session'):
                move = self._session._track_offset + 4
            else:
                move = 4
            num_of_tracks = len(self.song().tracks)
            if num_of_tracks >= move:
                move = move - 1
                self.song().view.selected_track = self.song().tracks[move]

    def track_select_3(self, value):
        if value > 0:
            if hasattr(self, '_session'):
                move = self._session._track_offset + 3
            else:
                move = 3
            num_of_tracks = len(self.song().tracks)
            if num_of_tracks >= move:
                move = move - 1
                self.song().view.selected_track = self.song().tracks[move]

    def track_select_2(self, value):
        if value > 0:
            if hasattr(self, '_session'):
                move = self._session._track_offset + 2
            else:
                move = 2
            num_of_tracks = len(self.song().tracks)
            if num_of_tracks >= move:
                move = move - 1
                self.song().view.selected_track = self.song().tracks[move]

    def track_select_1(self, value):
        if value > 0:
            if hasattr(self, '_session'):
                move = self._session._track_offset + 1
            else:
                move = 1
            num_of_tracks = len(self.song().tracks)
            if num_of_tracks >= move:
                move = move - 1
                self.song().view.selected_track = self.song().tracks[move]

    def tempo_fine_control_updown_mode0(self, value):
        global direction_tempo_fine_control_updown_mode0
        global lv_tempo_fine_control_updown_mode0
        if value == lv_tempo_fine_control_updown_mode0 and lv_tempo_fine_control_updown_mode0 != 0:
            if direction_tempo_fine_control_updown_mode0 == 'up':
                self._tempo_fine_control_up_value_mode0(1)
            elif direction_tempo_fine_control_updown_mode0 == 'down':
                self._tempo_fine_control_down_value_mode0(1)
            else:
                self._tempo_fine_control_up_value_mode0(1)
        else:
            if value > lv_tempo_fine_control_updown_mode0 and lv_tempo_fine_control_updown_mode0 != 0:
                self._tempo_fine_control_down_value_mode0(1)
                direction_tempo_fine_control_updown_mode0 = 'down'
            else:
                if value < lv_tempo_fine_control_updown_mode0 and lv_tempo_fine_control_updown_mode0 != 0:
                    self._tempo_fine_control_up_value_mode0(1)
                    direction_tempo_fine_control_updown_mode0 = 'up'
        lv_tempo_fine_control_updown_mode0 = value

    def _tempo_fine_control_up_value_mode0(self, value):
        if value:
            if self.song().tempo < 999:
                self.song().tempo = self.song().tempo + 0.1

    def _tempo_fine_control_down_value_mode0(self, value):
        if value:
            if self.song().tempo > 20:
                self.song().tempo = self.song().tempo - 0.1

    def tempo_control_updown_mode0(self, value):
        global direction_tempo_control_updown_mode0
        global lv_tempo_control_updown_mode0
        if value == lv_tempo_control_updown_mode0 and lv_tempo_control_updown_mode0 != 0:
            if direction_tempo_control_updown_mode0 == 'up':
                self._tempo_control_up_value_mode0(1)
            elif direction_tempo_control_updown_mode0 == 'down':
                self._tempo_control_down_value_mode0(1)
            else:
                self._tempo_control_up_value_mode0(1)
        else:
            if value > lv_tempo_control_updown_mode0 and lv_tempo_control_updown_mode0 != 0:
                self._tempo_control_down_value_mode0(1)
                direction_tempo_control_updown_mode0 = 'down'
            else:
                if value < lv_tempo_control_updown_mode0 and lv_tempo_control_updown_mode0 != 0:
                    self._tempo_control_up_value_mode0(1)
                    direction_tempo_control_updown_mode0 = 'up'
        lv_tempo_control_updown_mode0 = value

    def _tempo_control_up_value_mode0(self, value):
        if value:
            if self.song().tempo < 999:
                self.song().tempo = self.song().tempo + 1

    def _tempo_control_down_value_mode0(self, value):
        if value:
            if self.song().tempo > 22:
                self.song().tempo = self.song().tempo - 1

    def _trackleft_track_nav(self, value):
        if value > 0:
            track_idx = self.selected_track_idx() - 1
            if track_idx > 0:
                self.song().view.selected_track = self.song().tracks[(track_idx - 1)]

    def _trackright_track_nav(self, value):
        if value > 0:
            track_idx = self.selected_track_idx()
            num_of_tracks = len(self.song().tracks)
            if track_idx < num_of_tracks:
                track_idx = self.selected_track_idx() - 1
                self.song().view.selected_track = self.song().tracks[(track_idx + 1)]

    def _on_selected_track_changed(self):
        ControlSurface._on_selected_track_changed(self)
        self._display_reset_delay = 0
        value = 'selected track changed'
        if hasattr(self, '_set_track_select_led'):
            self._set_track_select_led()
        if hasattr(self, '_reload_active_devices'):
            self._reload_active_devices(value)
        if hasattr(self, 'update_all_ab_select_LEDs'):
            self.update_all_ab_select_LEDs(1)

    def _is_prev_device_on_or_off(self):
        self._device = self.song().view.selected_track.view.selected_device
        self._device_position = self.selected_device_idx()
        if self._device is None or self._device_position == 0:
            on_off = 'off'
        else:
            on_off = 'on'
        return on_off

    def _is_nxt_device_on_or_off(self):
        self._selected_device = self.selected_device_idx() + 1
        if self._device is None or self._selected_device == len(self.song().view.selected_track.devices):
            on_off = 'off'
        else:
            on_off = 'on'
        return on_off

    def _set_active_mode(self):
        if active_mode == '_mode2':
            self._mode2()
        else:
            if active_mode == '_mode1':
                self._mode1()
            else:
                if active_mode == '_mode0':
                    self._mode0()
        if hasattr(self, '_set_track_select_led'):
            self._set_track_select_led()
        if hasattr(self, '_turn_on_device_select_leds'):
            self._turn_off_device_select_leds()
            self._turn_on_device_select_leds()
        if hasattr(self, '_all_prev_device_leds'):
            self._all_prev_device_leds()
        if hasattr(self, '_all_nxt_device_leds'):
            self._all_nxt_device_leds()
        if hasattr(self, 'update_all_ab_select_LEDs'):
            self.update_all_ab_select_LEDs(1)

    def _remove_active_mode(self):
        if active_mode == '_mode2':
            self._remove_mode2()
        else:
            if active_mode == '_mode1':
                self._remove_mode1()
            else:
                if active_mode == '_mode0':
                    self._remove_mode0()

    def _activate_mode2(self, value):
        global active_mode
        global shift_previous_is_active
        if value > 0:
            shift_previous_is_active = 'off'
            self._remove_active_mode()
            active_mode = '_mode2'
            self._set_active_mode()

    def _activate_mode1(self, value):
        global active_mode
        global shift_previous_is_active
        if value > 0:
            shift_previous_is_active = 'off'
            self._remove_active_mode()
            active_mode = '_mode1'
            self._set_active_mode()

    def _activate_mode0(self, value):
        global active_mode
        global shift_previous_is_active
        if value > 0:
            shift_previous_is_active = 'off'
            self._remove_active_mode()
            active_mode = '_mode0'
            self._set_active_mode()

    def _activate_shift_mode2(self, value):
        global active_mode
        global previous_shift_mode2
        global shift_previous_is_active
        if value > 0:
            shift_previous_is_active = 'on'
            previous_shift_mode2 = active_mode
            self._remove_active_mode()
            active_mode = '_mode2'
            self._set_active_mode()
        else:
            if shift_previous_is_active == 'on':
                try:
                    previous_shift_mode2
                except NameError:
                    self.log_message('previous shift mode not defined yet')
                else:
                    self._remove_active_mode()
                    active_mode = previous_shift_mode2
                    self._set_active_mode()

    def _activate_shift_mode1(self, value):
        global active_mode
        global previous_shift_mode1
        global shift_previous_is_active
        if value > 0:
            shift_previous_is_active = 'on'
            previous_shift_mode1 = active_mode
            self._remove_active_mode()
            active_mode = '_mode1'
            self._set_active_mode()
        else:
            if shift_previous_is_active == 'on':
                try:
                    previous_shift_mode1
                except NameError:
                    self.log_message('previous shift mode not defined yet')
                else:
                    self._remove_active_mode()
                    active_mode = previous_shift_mode1
                    self._set_active_mode()

    def _activate_shift_mode0(self, value):
        global active_mode
        global previous_shift_mode0
        global shift_previous_is_active
        if value > 0:
            shift_previous_is_active = 'on'
            previous_shift_mode0 = active_mode
            self._remove_active_mode()
            active_mode = '_mode0'
            self._set_active_mode()
        else:
            if shift_previous_is_active == 'on':
                try:
                    previous_shift_mode0
                except NameError:
                    self.log_message('previous shift mode not defined yet')
                else:
                    self._remove_active_mode()
                    active_mode = previous_shift_mode0
                    self._set_active_mode()

    def selected_device_idx(self):
        self._device = self.song().view.selected_track.view.selected_device
        return self.tuple_index(self.song().view.selected_track.devices, self._device)

    def selected_track_idx(self):
        self._track = self.song().view.selected_track
        self._track_num = self.tuple_index(self.song().tracks, self._track)
        self._track_num = self._track_num + 1
        return self._track_num

    def tuple_index(self, tuple, obj):
        for i in xrange(0, len(tuple)):
            if tuple[i] == obj:
                return i

        return False

    def disconnect(self):
        super(hercules_p32_dj, self).disconnect()