import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:notes_app/domain/usecases/get_notes_use_case.dart';
import '../../domain/entities/note.dart';

abstract class NoteEvent {}

class LoadNotes extends NoteEvent {}

abstract class NoteState {}

class NoteInitial extends NoteState {}

class NoteLoading extends NoteState {}

class NoteLoaded extends NoteState {
  final List<Note> notes;

  NoteLoaded(this.notes);
}

class NoteBloc extends Bloc<NoteEvent, NoteState> {
  final GetNotesUseCase getNotesUseCase;

  NoteBloc(this.getNotesUseCase) : super(NoteInitial()) {
    on<LoadNotes>((event, emit) async {
      emit(NoteLoading());

      final notes = await getNotesUseCase.call();

      emit(NoteLoaded(notes));
    });
  }
}