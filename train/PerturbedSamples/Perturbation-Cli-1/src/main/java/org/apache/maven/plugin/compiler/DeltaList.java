[P11_Insert_Donor_Statement]^this.removed = new ArrayList<> ( oldList ) ;this.added = new ArrayList<> ( newList ) ;^36^^^^^35^41^this.added = new ArrayList<> ( newList ) ;^[CLASS] DeltaList  [METHOD] <init> [RETURN_TYPE] Collection)   Collection<E> oldList Collection<E> newList [VARIABLES] Collection  newList  oldList  List  added  removed  boolean  hasChanged  
[P1_Replace_Type]^this.added = new  Set <> ( newList ) ;^36^^^^^35^41^this.added = new ArrayList<> ( newList ) ;^[CLASS] DeltaList  [METHOD] <init> [RETURN_TYPE] Collection)   Collection<E> oldList Collection<E> newList [VARIABLES] Collection  newList  oldList  List  added  removed  boolean  hasChanged  
[P11_Insert_Donor_Statement]^this.added = new ArrayList<> ( newList ) ;this.removed = new ArrayList<> ( oldList ) ;^37^^^^^35^41^this.removed = new ArrayList<> ( oldList ) ;^[CLASS] DeltaList  [METHOD] <init> [RETURN_TYPE] Collection)   Collection<E> oldList Collection<E> newList [VARIABLES] Collection  newList  oldList  List  added  removed  boolean  hasChanged  
[P1_Replace_Type]^this.removed = new  List <> ( oldList ) ;^37^^^^^35^41^this.removed = new ArrayList<> ( oldList ) ;^[CLASS] DeltaList  [METHOD] <init> [RETURN_TYPE] Collection)   Collection<E> oldList Collection<E> newList [VARIABLES] Collection  newList  oldList  List  added  removed  boolean  hasChanged  
[P14_Delete_Statement]^^38^39^^^^35^41^added.removeAll ( oldList ) ; removed.removeAll ( newList ) ;^[CLASS] DeltaList  [METHOD] <init> [RETURN_TYPE] Collection)   Collection<E> oldList Collection<E> newList [VARIABLES] Collection  newList  oldList  List  added  removed  boolean  hasChanged  
[P11_Insert_Donor_Statement]^removed.removeAll ( newList ) ;added.removeAll ( oldList ) ;^38^^^^^35^41^added.removeAll ( oldList ) ;^[CLASS] DeltaList  [METHOD] <init> [RETURN_TYPE] Collection)   Collection<E> oldList Collection<E> newList [VARIABLES] Collection  newList  oldList  List  added  removed  boolean  hasChanged  
[P14_Delete_Statement]^^39^^^^^35^41^removed.removeAll ( newList ) ;^[CLASS] DeltaList  [METHOD] <init> [RETURN_TYPE] Collection)   Collection<E> oldList Collection<E> newList [VARIABLES] Collection  newList  oldList  List  added  removed  boolean  hasChanged  
[P11_Insert_Donor_Statement]^added.removeAll ( oldList ) ;removed.removeAll ( newList ) ;^39^^^^^35^41^removed.removeAll ( newList ) ;^[CLASS] DeltaList  [METHOD] <init> [RETURN_TYPE] Collection)   Collection<E> oldList Collection<E> newList [VARIABLES] Collection  newList  oldList  List  added  removed  boolean  hasChanged  
[P14_Delete_Statement]^^40^^^^^35^41^this.hasChanged = !added.isEmpty (  )  || !removed.isEmpty (  ) ;^[CLASS] DeltaList  [METHOD] <init> [RETURN_TYPE] Collection)   Collection<E> oldList Collection<E> newList [VARIABLES] Collection  newList  oldList  List  added  removed  boolean  hasChanged  
[P14_Delete_Statement]^^44^45^^^^43^45^return Collections.unmodifiableCollection ( added ) ; }^[CLASS] DeltaList  [METHOD] getAdded [RETURN_TYPE] Collection   [VARIABLES] List  added  removed  boolean  hasChanged  
[P14_Delete_Statement]^^48^49^^^^47^49^return Collections.unmodifiableCollection ( removed ) ; }^[CLASS] DeltaList  [METHOD] getRemoved [RETURN_TYPE] Collection   [VARIABLES] List  added  removed  boolean  hasChanged  