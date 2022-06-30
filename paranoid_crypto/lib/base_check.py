"""Module containing base class to be inherited by Paranoid check classes."""

from typing import List, Optional, Union
from paranoid_crypto import paranoid_pb2

# Type annotations covering the different types of crypto artfifacts
KeyListType = Union[List[paranoid_pb2.RSAKey], List[paranoid_pb2.ECKey]]
SigListType = Union[List[paranoid_pb2.RSASignature],
                    List[paranoid_pb2.ECDSASignature]]
ArtifactListType = Union[KeyListType, SigListType]


class BaseCheck(object):
  """Base class for Paranoid checks.

  Attributes:
    check_name: Public attribute containing the name of the check (string type).
    severity: Public attribute, containing the severity of the test
      (paranoid_pb2.SeverityType type). Subclasses must specify the severity in
      their constructors.
  """

  def __init__(self, severity: Optional["paranoid_pb2.SeverityType"] = None):
    """BaseCheck constructor.

    Args:
      severity: The severity of the test. Subclasses must specify their severity
        and pass to this constructor.
    """
    self.check_name = self.__class__.__name__  # A subclass takes its own name
    self.severity = severity

  def _CreateTestResult(self) -> paranoid_pb2.TestResultsEntry:
    """Returns a paranoid_pb2.TestResultsEntry protobuf ready for the checks.

    The created paranoid_pb2.TestResultsEntry is appropriate to be used on tests
    and have the paranoid_pb2.TestResultsEntry.result filled by the Check
    function (i.e., set as weak or not).

    Returns:
        A paranoid_pb2.TestResultsEntry protobuf ready for the checks. The
        initial result value is False, whereas the other attributes values are
        obtained from the object itself.

    Raises:
      KeyError: If the severity was not specified by the subclass.
    """

    if self.severity is None:
      raise KeyError("Please specify self.severity for %s." % self.check_name)
    return paranoid_pb2.TestResultsEntry(
        severity=self.severity, test_name=self.check_name, result=False)

  def Check(self, artifacts: ArtifactListType) -> bool:
    """Runs the check among the artifacts (keys/signatures).

    Args:
      artifacts: list of keys/signatures to be tested.

    Returns:
      A boolean indicating if at least one of the keys/signatures is weak.
    """
    raise NotImplementedError("Subclass didn't implement Check method.")