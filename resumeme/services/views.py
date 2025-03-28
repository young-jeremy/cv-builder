from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import DiscipleshipTrack, TrackNote
from .forms import DiscipleshipTrackForm, TrackNoteForm


def track_detail(request, slug):
    track = get_object_or_404(DiscipleshipTrack, slug=slug)
    notes = track.notes.all().order_by('-created_at')
    note_form = TrackNoteForm()

    context = {
        'track': track,
        'notes': notes,
        'note_form': note_form,
    }
    return render(request, 'services/track_detail.html', context)


@login_required
def add_track_note(request, slug):
    track = get_object_or_404(DiscipleshipTrack, slug=slug)

    if request.method == 'POST':
        form = TrackNoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.track = track
            note.save()
            messages.success(request, 'Note added successfully!')
        else:
            # Add more detailed error messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")

            # If no specific field errors, show a general error
            if not form.errors:
                messages.error(request, 'There was an error adding your note.')

            # Pass the form back to the template with errors
            return render(request, 'services/track_detail.html', {
                'track': track,
                'notes': track.notes.all().order_by('-created_at'),
                'note_form': form,
            })

    return redirect('services:track_detail', slug=slug)

